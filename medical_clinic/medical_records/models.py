from django.db import models
from doctors.models import Doctor
from patients.models import Patient
from appointments.models import Appointment

class MedicalRecord(models.Model):
    """Modelo para prontuários médicos"""
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT, related_name='medical_records', verbose_name="Paciente")
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name='medical_record', verbose_name="Consulta")
    doctor = models.ForeignKey(Doctor, on_delete=models.PROTECT, related_name='medical_records', verbose_name="Médico")
    date = models.DateField(auto_now_add=True, verbose_name="Data")
    main_complaint = models.TextField(verbose_name="Queixa Principal")
    history = models.TextField(verbose_name="História da Doença Atual")
    physical_exam = models.TextField(blank=True, null=True, verbose_name="Exame Físico")
    diagnosis = models.TextField(verbose_name="Diagnóstico")
    treatment = models.TextField(verbose_name="Tratamento")
    observations = models.TextField(blank=True, null=True, verbose_name="Observações")
    
    # Informações do sistema
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")
    
    def __str__(self):
        return f"Prontuário - {self.patient} - {self.date}"
    
    class Meta:
        verbose_name = "Prontuário"
        verbose_name_plural = "Prontuários"

class Prescription(models.Model):
    """Modelo para prescrições médicas"""
    medical_record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE, related_name='prescriptions', verbose_name="Prontuário")
    medicines = models.TextField(verbose_name="Medicamentos")
    dosage = models.TextField(verbose_name="Posologia")
    duration = models.TextField(verbose_name="Duração")
    notes = models.TextField(blank=True, null=True, verbose_name="Observações")
    
    # Informações do sistema
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    
    def __str__(self):
        return f"Prescrição - {self.medical_record.patient} - {self.created_at.date()}"
    
    class Meta:
        verbose_name = "Prescrição"
        verbose_name_plural = "Prescrições"

class ExamRequest(models.Model):
    """Modelo para solicitações de exames"""
    STATUS_CHOICES = [
        ('SOLICITADO', 'Solicitado'),
        ('AGENDADO', 'Agendado'),
        ('REALIZADO', 'Realizado'),
        ('CANCELADO', 'Cancelado'),
    ]
    
    medical_record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE, related_name='exam_requests', verbose_name="Prontuário")
    exam_name = models.CharField(max_length=100, verbose_name="Nome do Exame")
    instructions = models.TextField(blank=True, null=True, verbose_name="Instruções")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='SOLICITADO', verbose_name="Status")
    exam_date = models.DateField(blank=True, null=True, verbose_name="Data do Exame")
    result = models.TextField(blank=True, null=True, verbose_name="Resultado")
    result_date = models.DateField(blank=True, null=True, verbose_name="Data do Resultado")
    file = models.FileField(upload_to='exams/', blank=True, null=True, verbose_name="Arquivo")
    
    # Informações do sistema
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")
    
    def __str__(self):
        return f"{self.exam_name} - {self.medical_record.patient} - {self.created_at.date()}"
    
    class Meta:
        verbose_name = "Solicitação de Exame"
        verbose_name_plural = "Solicitações de Exames"