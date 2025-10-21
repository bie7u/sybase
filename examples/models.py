"""
Example Django models using Sybase backend.
"""
from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    """
    Author model.
    """
    name = models.CharField(max_length=100, db_index=True)
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True)
    birth_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'authors'
        ordering = ['name']
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'
    
    def __str__(self):
        return self.name


class Publisher(models.Model):
    """
    Publisher model.
    """
    name = models.CharField(max_length=200, unique=True)
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)
    founded_year = models.IntegerField(null=True, blank=True)
    
    class Meta:
        db_table = 'publishers'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Book(models.Model):
    """
    Book model with foreign key relationships.
    """
    title = models.CharField(max_length=200, db_index=True)
    author = models.ForeignKey(
        Author, 
        on_delete=models.CASCADE,
        related_name='books'
    )
    publisher = models.ForeignKey(
        Publisher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='books'
    )
    isbn = models.CharField(max_length=13, unique=True)
    published_date = models.DateField()
    pages = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    cover_image = models.CharField(max_length=255, blank=True)  # File path
    language = models.CharField(max_length=50, default='English')
    edition = models.IntegerField(default=1)
    in_stock = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'books'
        ordering = ['-published_date', 'title']
        indexes = [
            models.Index(fields=['title', 'author']),
            models.Index(fields=['published_date']),
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(pages__gt=0),
                name='books_pages_positive'
            ),
            models.CheckConstraint(
                check=models.Q(price__gte=0),
                name='books_price_non_negative'
            ),
        ]
    
    def __str__(self):
        return f"{self.title} by {self.author.name}"


class Review(models.Model):
    """
    Book review model.
    """
    RATING_CHOICES = [
        (1, 'Poor'),
        (2, 'Fair'),
        (3, 'Good'),
        (4, 'Very Good'),
        (5, 'Excellent'),
    ]
    
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    reviewer_name = models.CharField(max_length=100)
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField()
    review_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'reviews'
        ordering = ['-review_date']
        indexes = [
            models.Index(fields=['book', 'rating']),
        ]
    
    def __str__(self):
        return f"Review of {self.book.title} by {self.reviewer_name}"


class OrderItem(models.Model):
    """
    Order item model demonstrating various field types.
    """
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=0.00
    )
    total = models.DecimalField(max_digits=10, decimal_places=2)
    ordered_at = models.DateTimeField(auto_now_add=True)
    shipped_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'order_items'
        ordering = ['-ordered_at']
    
    def save(self, *args, **kwargs):
        """Calculate total before saving."""
        self.total = (self.unit_price * self.quantity) - self.discount
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.quantity}x {self.book.title}"


# Example queries
def example_queries():
    """
    Example queries demonstrating Django ORM with Sybase.
    """
    
    # Create
    author = Author.objects.create(
        name='John Doe',
        email='john@example.com',
        bio='Famous author'
    )
    
    publisher = Publisher.objects.create(
        name='Great Books Publishing',
        city='New York',
        country='USA'
    )
    
    book = Book.objects.create(
        title='Python Programming',
        author=author,
        publisher=publisher,
        isbn='9781234567890',
        published_date='2025-01-01',
        pages=350,
        price=49.99
    )
    
    # Read
    all_books = Book.objects.all()
    book = Book.objects.get(isbn='9781234567890')
    expensive_books = Book.objects.filter(price__gt=30)
    
    # Update
    book.price = 39.99
    book.save()
    
    # Bulk update
    Book.objects.filter(author=author).update(in_stock=True)
    
    # Delete
    Review.objects.filter(rating__lt=2).delete()
    
    # Complex queries
    from django.db.models import Q, Count, Avg, Sum
    
    # OR queries
    books = Book.objects.filter(
        Q(price__lt=30) | Q(author__name__icontains='doe')
    )
    
    # Aggregation
    avg_price = Book.objects.aggregate(Avg('price'))
    total_pages = Book.objects.aggregate(Sum('pages'))
    
    # Annotation
    authors_with_book_count = Author.objects.annotate(
        num_books=Count('books')
    ).filter(num_books__gt=0)
    
    # Joins (via select_related and prefetch_related)
    books_with_author = Book.objects.select_related('author', 'publisher').all()
    authors_with_books = Author.objects.prefetch_related('books').all()
    
    # Ordering
    recent_books = Book.objects.order_by('-published_date')[:10]
    
    # Distinct
    languages = Book.objects.values_list('language', flat=True).distinct()
    
    # F expressions
    from django.db.models import F
    
    # Increase all prices by 10%
    Book.objects.update(price=F('price') * 1.1)
    
    # Date queries
    from datetime import datetime, timedelta
    
    recent = datetime.now() - timedelta(days=365)
    recent_books = Book.objects.filter(published_date__gte=recent)
    
    # Year/month filtering
    books_2024 = Book.objects.filter(published_date__year=2024)
    books_jan = Book.objects.filter(published_date__month=1)
    
    return books
