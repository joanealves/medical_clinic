from django.db import models
from doctors.models import Doctor
from patients.models import Patient

class Appointment(models.Model):
    """Modelo para agendamento de consultas"""
    STATUS_CHOICES = [
        ('AGENDADO', 'Agendado'),
        ('CONFIRMADO', 'Confirmado'),
        ('CANCELADO', 'Cancelado'),
        ('CONCLUIDO', 'Concluído'),
        ('FALTOU', 'Não Compareceu'),
    ]
    
    doctor = models.ForeignKey(Doctor, on_delete=models.PROTECT, related_name='appointments', verbose_name="Médico")
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT, related_name='appointments', verbose_name="Paciente")
    date = models.DateField(verbose_name="Data")
    start_time = models.TimeField(verbose_name="Hora de Início")
    end_time = models.TimeField(verbose_name="Hora de Término")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='AGENDADO', verbose_name="Status")
    notes = models.TextField(blank=True, null=True, verbose_name="Observações")
    
    # Informações do pagamento
    payment_completed = models.BooleanField(default=False, verbose_name="Pagamento Concluído")
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Valor")
    payment_method = models.CharField(max_length=50, blank=True, null=True, verbose_name="Método de Pagamento")
    
    # Informações do sistema
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")
    
    def __str__(self):
        return f"{self.patient} - Dr(a). {self.doctor} - {self.date} {self.start_time}"
    
    class Meta:
        verbose_name = "Consulta"
        verbose_name_plural = "Consultas"
        # Garantir que não exista outro agendamento para o mesmo médico no mesmo horário
        unique_together = ('doctor', 'date', 'start_time')

class Notification(models.Model):
    """Modelo para notificações de agendamentos"""
    TYPE_CHOICES = [
        ('EMAIL', 'E-mail'),
        ('SMS', 'SMS'),
        ('WHATSAPP', 'WhatsApp'),
    ]
    
    STATUS_CHOICES = [
        ('PENDENTE', 'Pendente'),
        ('ENVIADO', 'Enviado'),
        ('FALHA', 'Falha'),
    ]
    
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='notifications', verbose_name="Consulta")
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name="Tipo")
    message = models.TextField(verbose_name="Mensagem")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDENTE', verbose_name="Status")
    sent_at = models.DateTimeField(blank=True, null=True, verbose_name="Enviado em")
    
    def __str__(self):
        return f"{self.appointment} - {self.get_type_display()} - {self.get_status_display()}"
    
    class Meta:
        verbose_name = "Notificação"
        verbose_name_plural = "Notificações"