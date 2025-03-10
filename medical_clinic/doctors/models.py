from django.db import models
from django.core.validators import RegexValidator

class Specialty(models.Model):
    """Modelo para especialidades médicas"""
    name = models.CharField(max_length=100, verbose_name="Nome da Especialidade")
    description = models.TextField(blank=True, null=True, verbose_name="Descrição")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Especialidade"
        verbose_name_plural = "Especialidades"

class Doctor(models.Model):
    """Modelo para cadastro de médicos"""
    # Validadores
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="O número de telefone deve estar no formato: '+999999999'. Até 15 dígitos permitidos."
    )
    cpf_regex = RegexValidator(
        regex=r'^\d{3}\.\d{3}\.\d{3}-\d{2}$',
        message="CPF deve estar no formato: '000.000.000-00'"
    )
    crm_regex = RegexValidator(
        regex=r'^\d{4,6}\/[A-Z]{2}$',
        message="CRM deve estar no formato: '00000/UF'"
    )
    
    # Informações básicas
    first_name = models.CharField(max_length=100, verbose_name="Nome")
    last_name = models.CharField(max_length=100, verbose_name="Sobrenome")
    cpf = models.CharField(max_length=14, validators=[cpf_regex], unique=True, verbose_name="CPF")
    crm = models.CharField(max_length=10, validators=[crm_regex], unique=True, verbose_name="CRM")
    specialties = models.ManyToManyField(Specialty, related_name='doctors', verbose_name="Especialidades")
    
    # Informações de contato
    email = models.EmailField(unique=True, verbose_name="E-mail")
    phone = models.CharField(validators=[phone_regex], max_length=17, verbose_name="Telefone")
    
    # Endereço
    address = models.CharField(max_length=200, verbose_name="Endereço")
    address_number = models.CharField(max_length=20, verbose_name="Número")
    complement = models.CharField(max_length=100, blank=True, null=True, verbose_name="Complemento")
    neighborhood = models.CharField(max_length=100, verbose_name="Bairro")
    city = models.CharField(max_length=100, verbose_name="Cidade")
    state = models.CharField(max_length=2, verbose_name="Estado")
    zip_code = models.CharField(max_length=9, verbose_name="CEP")
    
    # Informações profissionais
    biography = models.TextField(blank=True, null=True, verbose_name="Biografia")
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor da Consulta")
    
    # Informações do sistema
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")
    active = models.BooleanField(default=True, verbose_name="Ativo")
    
    def __str__(self):
        return f"Dr(a). {self.first_name} {self.last_name} - CRM: {self.crm}"
    
    class Meta:
        verbose_name = "Médico"
        verbose_name_plural = "Médicos"

class DoctorSchedule(models.Model):
    """Modelo para agenda dos médicos"""
    WEEKDAY_CHOICES = [
        (0, 'Segunda-feira'),
        (1, 'Terça-feira'),
        (2, 'Quarta-feira'),
        (3, 'Quinta-feira'),
        (4, 'Sexta-feira'),
        (5, 'Sábado'),
        (6, 'Domingo'),
    ]
    
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='schedules', verbose_name="Médico")
    weekday = models.IntegerField(choices=WEEKDAY_CHOICES, verbose_name="Dia da Semana")
    start_time = models.TimeField(verbose_name="Hora de Início")
    end_time = models.TimeField(verbose_name="Hora de Término")
    
    class Meta:
        verbose_name = "Horário do Médico"
        verbose_name_plural = "Horários dos Médicos"
        unique_together = ('doctor', 'weekday', 'start_time', 'end_time')
    
    def __str__(self):
        return f"{self.doctor} - {self.get_weekday_display()} ({self.start_time} - {self.end_time})"