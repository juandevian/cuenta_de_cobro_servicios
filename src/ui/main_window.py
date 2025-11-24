"""
Ventana principal de la aplicación de importación de facturas
"""
import pathlib
import logging
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QFileDialog, QLabel, QTextEdit, QProgressBar,
                             QMessageBox, QGroupBox, QTabWidget,
                             QTableWidget, QTableWidgetItem)
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QFont, QIcon

# Imports relativos al paquete
from typing import Any
from ..services.invoice_item_processor import InvoiceItemProcessor
from ..services.excel_handler import ExcelHandler
from ..config.config import Config
from ..utils import resource_path
from ..services.create_excels import create_sample_excel, create_excel_import_template

# Configurar logging
logging.basicConfig(level=getattr(logging, Config.LOG_LEVEL))
logger = logging.getLogger(__name__)

class ImportWorker(QThread):
    """Worker thread para la importación de datos"""
    progress_updated = pyqtSignal(int, str)
    import_finished = pyqtSignal(dict)

    def __init__(self, file_path: str | pathlib.Path, processor: InvoiceItemProcessor):
        super().__init__()
        self.file_path = file_path
        self.processor = processor

    def run(self):
        """Ejecuta la importación en un hilo separado"""
        try:
            file_path_str = str(self.file_path)
            result = self.processor.process_excel_import(file_path_str)
            self.import_finished.emit(result)
        except Exception as e:
            logger.error(f"Error en el worker de importación: {e}")
            self.import_finished.emit({
                'success': False,
                'message': f'Error: {str(e)}',
                'processed': 0,
                'errors': [str(e)],
                'warnings': []
            })

class MainWindow(QMainWindow):
    """Ventana principal de la aplicación"""

    def __init__(self, excel_handler: ExcelHandler | None = None) -> None:
        super().__init__()
        self.processor: Any | None = None
        self.excel_handler: ExcelHandler = excel_handler or ExcelHandler()
        self.current_file_path: pathlib.Path | None = None
        self.init_ui()
        self.connect_to_database()

    def init_ui(self):
        """Inicializa la interfaz de usuario"""
        self.setWindowTitle(f"{Config.APP_NAME} v{Config.APP_VERSION}")
        self.setGeometry(100, 100, Config.WINDOW_WIDTH, Config.WINDOW_HEIGHT)

        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout principal
        main_layout = QVBoxLayout(central_widget)

        # Crear pestañas
        self.tab_widget = QTabWidget()

        # Pestaña de importación
        import_tab = self.create_import_tab()
        self.tab_widget.addTab(import_tab, "Importar Facturas")

         # Pestaña de información
        info_tab = self.create_info_tab()
        self.tab_widget.addTab(info_tab, "Información")

        main_layout.addWidget(self.tab_widget)

        # Barra de estado
        self.status_bar = self.statusBar()
        self.status_bar.showMessage("Listo")

    def create_import_tab(self):
        """Crea la pestaña de importación"""
        tab = QWidget()
        layout = QVBoxLayout(tab)

        # Grupo de selección de archivo
        file_group = QGroupBox("Seleccionar Archivo")
        file_layout = QVBoxLayout(file_group)

        # Botón para seleccionar archivo
        self.select_file_btn = QPushButton("Seleccionar Plantilla de Importación")
        self.select_file_btn.clicked.connect(self.select_file)
        file_layout.addWidget(self.select_file_btn)

        # Label para mostrar el archivo seleccionado
        self.file_label = QLabel("No se ha seleccionado ningún archivo")
        self.file_label.setWordWrap(True)
        file_layout.addWidget(self.file_label)

        # Botón para vista previa
        self.preview_btn = QPushButton("Vista Previa")
        self.preview_btn.clicked.connect(self.show_preview)
        self.preview_btn.setEnabled(False)
        file_layout.addWidget(self.preview_btn)

        layout.addWidget(file_group)

        # Grupo de acciones
        action_group = QGroupBox("Acciones")
        action_layout = QVBoxLayout(action_group)

        # Importar función de creación de plantillas
        btn_layout = QHBoxLayout()

        create_sample_excel_btn = QPushButton("Generar Plantilla de Ejemplo")
        create_sample_excel_btn.clicked.connect(lambda: self.generate_sample_excel())
        btn_layout.addWidget(create_sample_excel_btn)

        create_template_btn = QPushButton("Crear Plantilla de Importación")
        create_template_btn.clicked.connect(lambda: self.generate_template())
        create_template_btn.setStyleSheet("""
            QPushButton:hover {
                border-radius: 5px;
                background-color: #4CAF50;
                color: white;
                font-weight: bold;
            }
        """)
        btn_layout.addWidget(create_template_btn)

        action_layout.addLayout(btn_layout)

        self.import_btn = QPushButton("Importar Servicio a Cobrar")
        self.import_btn.clicked.connect(self.start_import)
        self.import_btn.setEnabled(False)
        self.import_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-weight: bold;
                padding: 10px;
                font-size: 14px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #45a049;
                border-radius: 10px;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
                border-radius: 10px;
            }
        """)
        action_layout.addWidget(self.import_btn)

        # Barra de progreso
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        action_layout.addWidget(self.progress_bar)

        layout.addWidget(action_group)

        # Registro de eventos/ log
        log_group = QGroupBox("Registro de Eventos")
        log_layout = QVBoxLayout(log_group)
        

        self.log_text = QTextEdit()
        self.log_text.setMaximumHeight(200)
        self.log_text.setReadOnly(True)
        log_layout.addWidget(self.log_text)

        # Botón para limpiar log
        clear_log_btn = QPushButton("Limpiar Registro")
        clear_log_btn.clicked.connect(self.clear_log)
        log_layout.addWidget(clear_log_btn)

        layout.addWidget(log_group)

        return tab

    def create_info_tab(self):
        """Crea la pestaña de información"""
        tab = QWidget()
        layout = QVBoxLayout(tab)

        # Información de la aplicación
        info_text = f"""
        <h3>{Config.APP_NAME} v{Config.APP_VERSION}</h3>
        <p>Sistema para importar servicios cobrados por consumo desde archivos Excel a <strong>Orión Plus</strong>.</p>
        <p><em>Copyright © 2026 - OptimuSoft SAS - Todos los derechos reservados.</em></p>

        <h4>Descripción General:</h4>
        <p>Módulo diseñado para importar servicios que basan su cobro en consumo (diferencia entre lectura actual y anterior), 
        calculando automáticamente el valor a facturar según el valor unitario definido.</p>

        <h4>Guía Rápida:</h4>
        <ol>
            <li>Use el botón "Crear Plantilla de Importación" para generar un archivo Excel en blanco</li>
            <li>Diligencie la plantilla con los datos de consumo (lecturas) y valores unitarios</li>
            <li>Importe el archivo usando "Seleccionar Plantilla de Importación"</li>
            <li>Verifique los datos en "Vista Previa" antes de importar</li>
            <li>Ejecute la importación con "Importar Servicio a Cobrar"</li>
        </ol>

        <h4>Datos Requeridos:</h4>
        <ul>
            <li>Identificadores (carpeta, servicio, predio o cliente)</li>
            <li>Periodo de cobro (AAAAMM)</li>
            <li>Lecturas (anterior y actual)</li>
            <li>Valor unitario del servicio</li>
        </ul>

        <p><strong>¿Necesita más información?</strong></p>
        <p>Consulte la <a href="https://www.notion.so/optimusoft/Gu-a-de-Importaci-n-de-Servicios-por-Consumo-292df310252780458c5ecbf6b2490ab4?source=copy_link">guía detallada de usuario</a> 
        para instrucciones completas sobre:</p>
        <ul>
            <li>Formato y validación detallada de datos</li>
            <li>Solución de problemas comunes</li>
        </ul>
        """

        self.info_label = QLabel(info_text)
        self.info_label.setWordWrap(True)
        self.info_label.setOpenExternalLinks(True)
        layout.addWidget(self.info_label)

        return tab

    def connect_to_database(self):
        """Conecta a la base de datos"""
        try:
            self.processor = InvoiceItemProcessor()
            if self.processor.db.connection and self.processor.db.connection.is_connected():
                self.log_message("Conexión a base de datos establecida", "INFO")
                self.status_bar.showMessage("Conectado a base de datos")
            else:
                self.log_message("Error al conectar con la base de datos", "ERROR")
                self.status_bar.showMessage("Error de conexión")
        except Exception as e:
            self.log_message(f"Error de conexión: {e}", "ERROR")
            self.status_bar.showMessage("Error de conexión")

    def generate_sample_excel(self):
        """Genera Excel de ejemplo con selección de ruta"""
        file_dialog = QFileDialog()
        output_path = file_dialog.getExistingDirectory(self, "Seleccionar carpeta para guardar Excel de ejemplo")
        if output_path:
            try:
                file_path = create_sample_excel(output_path)
                QMessageBox.information(self, "Éxito", f"Excel de ejemplo creado en: {file_path}")
                self.log_message(f"Excel de ejemplo creado: {file_path}", "INFO")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al crear Excel: {e}")
                self.log_message(f"Error al crear Excel de ejemplo: {e}", "ERROR")

    def generate_template(self):
        """Genera plantilla de importación con selección de ruta"""
        file_dialog = QFileDialog()
        output_path = file_dialog.getExistingDirectory(self, "Seleccionar carpeta para guardar plantilla de importación")
        if output_path:
            try:
                file_path = create_excel_import_template(output_path)
                QMessageBox.information(self, "Éxito", f"Plantilla de importación creada en: {file_path}")
                self.log_message(f"Plantilla de importación creada: {file_path}", "INFO")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al crear plantilla: {e}")
                self.log_message(f"Error al crear plantilla de importación: {e}", "ERROR")

    def select_file(self):
        """Abre diálogo para seleccionar archivo Excel"""
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(
            self,
            "Seleccionar Archivo Excel",
            "",
            f"Archivos Excel (*.xlsx *.xls);;Todos los archivos (*)"
        )

        if file_path:
            self.current_file_path = file_path
            self.file_label.setText(f"Archivo seleccionado: {file_path}")
            self.preview_btn.setEnabled(True)
            self.import_btn.setEnabled(True)
            self.log_message(f"Archivo seleccionado: {file_path}", "INFO")

    def show_preview(self):
        """Muestra vista previa del archivo Excel"""
        if not self.current_file_path:
            return

        try:
            preview_data = self.excel_handler.get_excel_preview(self.current_file_path)

            if preview_data:
                # Crear ventana de vista previa
                # Guardamos referencia en self para evitar GC que puede provocar cierres inesperados
                preview_window = QMainWindow(self)
                self.preview_window = preview_window
                preview_window.setWindowTitle("Vista Previa del Archivo Excel")
                preview_window.setGeometry(150, 150, 900, 600)

                central_widget = QWidget()
                preview_window.setCentralWidget(central_widget)
                layout = QVBoxLayout(central_widget)

                # Información del archivo
                info_text = f"""
                <b>Archivo:</b> {preview_data['filename']}<br>
                <b>Total de filas:</b> {preview_data['total_rows']}<br>
                <b>Columnas:</b> {', '.join(preview_data['columns'])}<br>
                <b>Tamaño:</b> {preview_data['file_size'] / 1024:.2f} KB
                """
                info_label = QLabel(info_text)
                layout.addWidget(info_label)

                # Tabla con datos de vista previa
                table = QTableWidget()
                table.setRowCount(len(preview_data['preview_data']))
                table.setColumnCount(len(preview_data['columns']))

                # Configurar headers
                table.setHorizontalHeaderLabels(preview_data['columns'])
                table.horizontalHeader().setStretchLastSection(True)

                # Llenar tabla con datos
                for row_idx, row_data in enumerate(preview_data['preview_data']):
                    for col_idx, column in enumerate(preview_data['columns']):
                        value = str(row_data.get(column, ''))
                        table.setItem(row_idx, col_idx, QTableWidgetItem(value))

                layout.addWidget(table)
                preview_window.show()

            else:
                QMessageBox.warning(self, "Error", "No se pudo obtener la vista previa del archivo")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al mostrar vista previa: {e}")

    def start_import(self):
        """Inicia el proceso de importación"""
        if not self.current_file_path:
            return

        # Primero validar
        validation_result = self.processor.validate_excel_only(str(self.current_file_path))
        
        if not validation_result['valid']:
            error_message = "Errores de validación encontrados:\n" + "\n".join(validation_result['errors'])
            QMessageBox.critical(self, "Errores de Validación", error_message)
            return
        
        # Si hay advertencias, mostrarlas y pedir confirmación
        if validation_result['warnings']:
            warning_message = "Advertencias encontradas:\n" + "\n".join(validation_result['warnings']) + "\n\n¿Desea continuar con la importación?"
            reply = QMessageBox.question(
                self,
                'Advertencias de Validación',
                warning_message,
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            if reply == QMessageBox.No:
                return

        # Confirmar importación
        reply = QMessageBox.question(
            self,
            'Confirmar Importación',
            '¿Está seguro de que desea importar las facturas desde el archivo Excel?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.Yes
        )

        if reply == QMessageBox.Yes:
            self.execute_import()

    def execute_import(self):
        """Ejecuta la importación en un hilo separado"""
        if not self.processor:
            QMessageBox.critical(self, "Error", "No hay conexión a la base de datos")
            return

        # Deshabilitar botones durante la importación
        self.import_btn.setEnabled(False)
        self.preview_btn.setEnabled(False)
        self.select_file_btn.setEnabled(False)

        # Mostrar barra de progreso
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # Indeterminada

        # Crear y ejecutar worker
        self.import_worker = ImportWorker(self.current_file_path, self.processor)
        self.import_worker.import_finished.connect(self.on_import_finished)
        self.import_worker.start()

        self.log_message("Iniciando importación...", "INFO")
        self.status_bar.showMessage("Importando...")

    def on_import_finished(self, result):
        """Maneja el resultado de la importación"""
        # Rehabilitar botones
        self.import_btn.setEnabled(True)
        self.preview_btn.setEnabled(True)
        self.select_file_btn.setEnabled(True)

        # Ocultar barra de progreso
        self.progress_bar.setVisible(False)

        # Mostrar resultado
        if result['success']:
            QMessageBox.information(
                self,
                "Importación Exitosa",
                f"{result['message']}\n\nFacturas procesadas: {result['processed']}"
            )
            self.log_message(result['message'], "INFO")

            if result['warnings']:
                for warning in result['warnings']:
                    self.log_message(f"Advertencia: {warning}", "WARNING")
        else:
            error_message = result['message']
            if result['errors']:
                error_message += "\n\nErrores encontrados:\n" + "\n".join(result['errors'])

            QMessageBox.critical(self, "Error en Importación", error_message)
            self.log_message(result['message'], "ERROR")

            if result['errors']:
                for error in result['errors']:
                    self.log_message(f"Error: {error}", "ERROR")

        self.status_bar.showMessage("Listo")

   
        """Prueba la conexión a la base de datos"""
        try:
            if self.processor and self.processor.db.connection and self.processor.db.connection.is_connected():
                QMessageBox.information(self, "Conexión", "Conexión a base de datos exitosa")
                self.log_message("Prueba de conexión exitosa", "INFO")
            else:
                QMessageBox.critical(self, "Error", "No se pudo conectar a la base de datos")
                self.log_message("Error en prueba de conexión", "ERROR")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error de conexión: {e}")
            self.log_message(f"Error en prueba de conexión: {e}", "ERROR")

    def log_message(self, message: str, level: str = "INFO"):
        """Agrega un mensaje al log"""
        timestamp = f"[{level}]"
        log_entry = f"{timestamp} {message}\n"
        self.log_text.append(log_entry)

        # Auto-scroll al final
        scrollbar = self.log_text.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def clear_log(self):
        """Limpia el área de log"""
        self.log_text.clear()

    def closeEvent(self, event):
        """Maneja el cierre de la aplicación"""
        if self.processor:
            self.processor.close()
        event.accept()