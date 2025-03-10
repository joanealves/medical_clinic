# patients/models.py
from django.db import models
from django.core.validators import RegexValidator

class HealthInsurance(models.Model):
    """Modelo para planos de saúde"""
    name = models.CharField(max_length=100, verbose_name="Nome do Convênio")
    plan_type = models.CharField(max_length=50, verbose_name="Tipo de Plano")
    registration_number = models.CharField(max_length=50, verbose_name="Número de Registro")
    active = models.BooleanField(default=True, verbose_name="Ativo")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Convênio"
        verbose_name_plural = "Convênios"

class Patient(models.Model):
    """Modelo para cadastro de pacientes"""
    GENDER_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('O', 'Outro'),
    ]
    
    BLOOD_TYPE_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]
    
    # Validadores
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="O número de telefone deve estar no formato: '+999999999'. Até 15 dígitos permitidos."
    )
    cpf_regex = RegexValidator(
        regex=r'^\d{3}\.\d{3}\.\d{3}-\d{2}$',
        message="CPF deve estar no formato: '000.000.000-00'"
    )
    
    # Informações básicas
    first_name = models.CharField(max_length=100, verbose_name="Nome")
    last_name = models.CharField(max_length=100, verbose_name="Sobrenome")
    cpf = models.CharField(max_length=14, validators=[cpf_regex], unique=True, verbose_name="CPF")
    birth_date = models.DateField(verbose_name="Data de Nascimento")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="Gênero")
    blood_type = models.CharField(max_length=3, choices=BLOOD_TYPE_CHOICES, blank=True, null=True, verbose_name="Tipo Sanguíneo")
    
    # Informações de contato
    email = models.EmailField(unique=True, verbose_name="E-mail")
    phone = models.CharField(validators=[phone_regex], max_length=17, verbose_name="Telefone")
    emergency_contact = models.CharField(validators=[phone_regex], max_length=17, verbose_name="Contato de Emergência")
    
    # Endereço
    address = models.CharField(max_length=200, verbose_name="Endereço")
    address_number = models.CharField(max_length=20, verbose_name="Número")
    complement = models.CharField(max_length=100, blank=True, null=True, verbose_name="Complemento")
    neighborhood = models.CharField(max_length=100, verbose_name="Bairro")
    city = models.CharField(max_length=100, verbose_name="Cidade")
    state = models.CharField(max_length=2, verbose_name="Estado")
    zip_code = models.CharField(max_length=9, verbose_name="CEP")
    
    # Informações médicas
    health_insurance = models.ForeignKey(HealthInsurance, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Convênio")
    insurance_number = models.CharField(max_length=50, blank=True, null=True, verbose_name="Número da Carteirinha")
    allergies = models.TextField(blank=True, null=True, verbose_name="Alergias")
    chronic_diseases = models.TextField(blank=True, null=True, verbose_name="Doenças Crônicas")
    
    # Informações do sistema
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")
    active = models.BooleanField(default=True, verbose_name="Ativo")
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.cpf}"
    
    class Meta:
        verbose_name = "Paciente"
        verbose_name_plural = "Pacientes"