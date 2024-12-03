from django.core.exceptions import ValidationError

def validate_pdf_file(value):
    if not value.name.endswith('.pdf'):
        raise ValidationError('Solo se permiten archivos PDF.')
    
def validate_image_file_extension(value):
    valid_extensions = ['.jpg', '.jpeg', '.png']
    if not value.name.lower().endswith(tuple(valid_extensions)):
        raise ValidationError('Solo se permiten archivos .jpg, .jpeg, .png')