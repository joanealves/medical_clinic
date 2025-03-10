from django.db import models
from patients.models import Patient, HealthInsurance
from doctors.models import Doctor
from appointments.models import Appointment

class Payment(models.Model):
    """Modelo para pagamentos"""
    PAYMENT_METHOD_CHOICES = [
        ('DINHEIRO', 'Dinheiro'),
        ('CARTAO_CREDITO', 'Cartão de Crédito'),
        ('CARTAO_DEBITO', 'Cartão de Débito'),
        ('PIX', 'PIX'),
        ('BOLETO', 'Boleto'),
        ('CONVENIO', 'Convênio'),
    ]
    
    STATUS_CHOICES = [
        ('PENDENTE', 'Pendente'),
        ('APROVADO', 'Aprovado'),
        ('RECUSADO', 'Recusado'),
        ('ESTORNADO', 'Estornado'),
    ]
    
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name='payment_details', verbose_name="Consulta")
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT, related_name='payments', verbose_name="Paciente")
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, verbose_name="Método de Pagamento")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor")
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Desconto")
    health_insurance = models.ForeignKey(HealthInsurance, on_delete=models.SET_NULL, blank=True, null=True, related_name='payments', verbose_name="Convênio")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDENTE', verbose_name="Status")
    payment_date = models.DateField(blank=True, null=True, verbose_name="Data de Pagamento")
    transaction_id = models.CharField(max_length=100, blank=True, null=True, verbose_name="ID da Transação")
    notes = models.TextField(blank=True, null=True, verbose_name="Observações")
    
    # Informações do sistema
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")
    
    def __str__(self):
        return f"Pagamento - {self.patient} - {self.appointment.date} - {self.amount}"
    
    class Meta:
        verbose_name = "Pagamento"
        verbose_name_plural = "Pagamentos"

class Expense(models.Model):
    """Modelo para despesas da clínica"""
    CATEGORY_CHOICES = [
        ('ALUGUEL', 'Aluguel'),
        ('ENERGIA', 'Energia'),
        ('AGUA', 'Água'),
        ('INTERNET', 'Internet'),
        ('TELEFONE', 'Telefone'),
        ('MATERIAL', 'Material de Escritório'),
        ('EQUIPAMENTO', 'Equipamento'),
        ('MANUTENCAO', 'Manutenção'),
        ('SALARIO', 'Salário'),
        ('IMPOSTO', 'Imposto'),
        ('OUTRO', 'Outro'),
    ]
    
    description = models.CharField(max_length=200, verbose_name="Descrição")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, verbose_name="Categoria")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor")
    due_date = models.DateField(verbose_name="Data de Vencimento")
    payment_date = models.DateField(blank=True, null=True, verbose_name="Data de Pagamento")
    paid = models.BooleanField(default=False, verbose_name="Pago")
    recurring = models.BooleanField(default=False, verbose_name="Recorrente")
    notes = models.TextField(blank=True, null=True, verbose_name="Observações")
    
    # Informações do sistema
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")
    
    def __str__(self):
        return f"{self.description} - {self.due_date} - R$ {self.amount}"
    
    class Meta:
        verbose_name = "Despesa"
        verbose_name_plural = "Despesas"

class DoctorPayment(models.Model):
    """Modelo para pagamentos aos médicos"""
    doctor = models.ForeignKey(Doctor, on_delete=models.PROTECT, related_name='payments', verbose_name="Médico")
    period_start = models.DateField(verbose_name="Início do Período")
    period_end = models.DateField(verbose_name="Fim do Período")
    consultations_count = models.IntegerField(verbose_name="Número de Consultas")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor Total")
    payment_date = models.DateField(blank=True, null=True, verbose_name="Data de Pagamento")
    paid = models.BooleanField(default=False, verbose_name="Pago")
    notes = models.TextField(blank=True, null=True, verbose_name="Observações")
    
    # Informações do sistema
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")
    
    def __str__(self):
        return f"Pagamento - Dr(a). {self.doctor} - {self.period_start} a {self.period_end}"
    
    class Meta:
        verbose_name = "Pagamento ao Médico"
        verbose_name_plural = "Pagamentos aos Médicos"