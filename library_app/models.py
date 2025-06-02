from django.db import models, transaction
from django.utils import timezone
from django.forms import ValidationError

from accounts_app.models import CustomUser

# Abstract timestamp model
class TimeStampField(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

# Choices
BookChoices = [
    ('NOVEL', 'Novel'),
    ('SCIENCE_BOOK', 'Science Book'),
    ('HISTORY', 'History'),
    ('MAGAZINES', 'Magazine'),
]

EbookChoices = [
    ('PDF', 'PDF'),
    ('EPUB', 'EPUB'),
]

BookTransactionChoices = [
    ('Borrow', 'Borrow'),
    ('Return', 'Return'),
]

# Models
class PhysicalBook(TimeStampField):
    title = models.CharField(max_length=400)
    type = models.CharField(max_length=50, choices=BookChoices)
    edition = models.IntegerField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    summary = models.TextField(max_length=500000, blank=True)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.title} by {self.author}'


class EBook(TimeStampField):
    title = models.CharField(max_length=400)
    file_format = models.CharField(max_length=50, choices=EbookChoices)
    download_link = models.URLField(blank=True)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.title} (eBook)'


class BookRecord(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    ebook = models.ForeignKey(EBook, on_delete=models.CASCADE, null=True, blank=True)
    physical_book = models.ForeignKey(PhysicalBook, on_delete=models.CASCADE, null=True, blank=True)
    borrow_date = models.DateTimeField(auto_now_add=True)
    is_due = models.DateTimeField()
    returned_date = models.DateTimeField(null=True, blank=True)
    transaction_type = models.CharField(max_length=20, choices=BookTransactionChoices)

    class Meta:
        ordering = ['-borrow_date']
        verbose_name = "Book Record"
        verbose_name_plural = "Book Records"

    def __str__(self):
        books = []
        if self.ebook:
            books.append(f"eBook: {self.ebook.title}")
        if self.physical_book:
            books.append(f"Physical Book: {self.physical_book.title}")
        if not books:
            books.append("No Book")

        status = "Returned" if self.returned_date else "Borrowed"
        return f'{self.user} - {status} {" & ".join(books)}'

    def is_overdue(self):
        return not self.returned_date and timezone.now() > self.is_due

    def clean(self):
        if not self.ebook and not self.physical_book:
            raise ValidationError("You must select at least one book (ebook or physical).")

        if self.ebook and self.ebook.quantity < 1:
            raise ValidationError('This eBook is currently unavailable.')

        if self.physical_book and self.physical_book.quantity < 1:
            raise ValidationError('This physical book is currently unavailable.')

    @transaction.atomic
    def save(self, *args, **kwargs):
        is_new = self.pk is None

        if is_new:
            # Borrowing: reduce quantity
            if self.physical_book:
                if self.physical_book.quantity < 1:
                    raise ValidationError("This physical book is out of stock.")
                self.physical_book.quantity -= 1
                self.physical_book.save()

            elif self.ebook:
                if self.ebook.quantity < 1:
                    raise ValidationError("This eBook is out of stock.")
                self.ebook.quantity -= 1
                self.ebook.save()

        else:
            # Returning: increase quantity
            original = BookRecord.objects.get(pk=self.pk)
            if not original.returned_date and self.returned_date:
                if self.physical_book:
                    self.physical_book.quantity += 1
                    self.physical_book.save()
                elif self.ebook:
                    self.ebook.quantity += 1
                    self.ebook.save()

        super().save(*args, **kwargs)
