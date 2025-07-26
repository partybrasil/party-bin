---
description: 'Chat mode personalizado para el proyecto PartyBin, una aplicación pastebin avanzada
  desarrollada en Flask con Python. Este modo guía a Copilot Chat GPT-4.1 para entender
  la estructura, funcionalidades y flujo de trabajo del proyecto PartyBin, facilitando
  la creación, edición y mantenimiento de código sin perder contexto'
tools: ['changes', 'codebase', 'editFiles', 'extensions', 'fetch', 'findTestFiles', 'githubRepo', 'new', 'openSimpleBrowser', 'problems', 'runCommands', 'runNotebooks', 'runTasks', 'runTests', 'search', 'searchResults', 'terminalLastCommand', 'terminalSelection', 'testFailure', 'usages', 'vscodeAPI', 'activePullRequest', 'copilotCodingAgent', 'configurePythonEnvironment', 'getPythonEnvironmentInfo', 'getPythonExecutableCommand', 'installPythonPackage']
---
# ChatMode para Copilot Chat GPT-4.1

# Proyecto: party-bin — Pastebin personal avanzado con Flask

---

## 1. Resumen general del proyecto party-bin

party-bin es una aplicación web de pastebin personal desarrollada con Python y Flask, diseñada para uso individual y alojada en servicios económicos como Render. Es un clon mejorado de Rentry con funcionalidades avanzadas y consumo muy bajo de recursos.

### Funcionalidades principales:

- Creación de pastes con texto plano, Markdown, HTML y código con resaltado de sintaxis automático
- Definición opcional de URLs personalizados para cada paste; si no se define, URL aleatorio generado automáticamente
- Auto destrucción configurable:
- Por tiempo (fecha/hora o cuenta regresiva)
- Por número de vistas (destruye cuando se alcanza el límite)
- Auto destrucción al primer acceso (one-time view)
- Edición de pastes protegida con contraseña (puede haber edición con o sin contraseña, código de edición al estilo Rentry)
- Protección completa opcional con contraseña que bloquea visualización y edición (misma contraseña)
- Temas visuales para la UI: Claro, Oscuro, Hacker-style (Monokai), fáciles de extender
- Vista previa automática de imágenes incrustadas (URLs directas, Imgur, base64)
- Contador en tiempo real de palabras y caracteres
- Firma opcional con alias o nombre sin necesidad de cuentas
- Modo “paste privado” que solo es accesible por enlace y no indexa
- Exportación de pastes a .txt, .md o .html con botón de descarga
- Vistas raw con botón de copiar al portapapeles
- Generación de código QR para compartir rápidamente
- Soporte para etiquetas/tags para organizar pastes
- Metadata visible: fecha de creación, última visualización, contador de vistas, expiración con cuenta regresiva
- Mini dashboard para gestionar pastes recientes con acceso por clave secreta, sin login
- Guardado de datos local (SQLite o ficheros) para funcionamiento offline y persistencia local
- Funcionalidad para correr la app localmente o desplegar en Render sin perder funcionalidad básica
- Diseño modular y limpio para fácil mantenimiento y extensión

---

## 2. Estructura típica del proyecto

```bash
party-bin/
│
├── app.py # Entrada principal de Flask
├── requirements.txt # Dependencias Python
├── config.py # Configuraciones generales y de entorno
├── models.py # Modelos de datos (Paste, Usuario, etc.)
├── routes/ # Blueprint con rutas de la app
│ ├── pastes.py
│ ├── auth.py
│ └── dashboard.py
├── static/ # Archivos estáticos (css, js, imágenes)
├── templates/ # Plantillas Jinja2 para renderizado
│ ├── base.html
│ ├── paste.html
│ ├── edit.html
│ └── dashboard.html
├── utils.py # Funciones auxiliares (validaciones, manejo de URLs, etc.)
├── data/ # Carpeta para base de datos local o archivos JSON
│ └── party-bin.db # SQLite por defecto
└── README.md # Documentación completa
```

---

## 3. Instrucciones para el modelo y flujo de interacción

### Cuando el usuario inicia la conversación:

- Lee el README.md completo y entiende cada funcionalidad descrita
- Recuerda la estructura y la organización modular
- Prepárate para responder preguntas técnicas o para iniciar la creación o modificación de código
- Si hay ambigüedades o falta información para una tarea, pide detalles concretos y ejemplos para evitar errores
- Si el usuario pide “empezar a programar” o “implementa tal funcionalidad”, confirma brevemente lo que va a hacer antes de generar código
- Para cada tarea o fragmento que generes, ofrece una explicación clara de lo que has hecho y cómo probarlo
- Asegúrate que el código respeta las mejores prácticas de Flask, seguridad, modularidad y rendimiento

### Reglas para edición y mantenimiento:

- Cuando el usuario solicite editar pastes, modifica las rutas, modelos y vistas relacionadas sin romper funcionalidades existentes
- Si hay cambios en el esquema de la base de datos, pregunta antes de hacer migraciones o actualizaciones
- Mantén el estilo de código consistente con Python y Flask idiomáticos
- Asegúrate que los controles de seguridad (contraseñas, acceso privado, autodestrucción) se mantengan robustos
- Para nuevas funcionalidades, crea funciones o módulos separados cuando sea posible para mantener limpieza

---

## 4. Recordatorios clave para mantener la coherencia

- URLs de pastes: personalizados o aleatorios (formato corto y único)
- Auto destrucción: combina timers y contadores de vistas, con limpieza automática en backend
- Contraseña: la misma para editar y proteger visualización si está activada la protección completa
- Temas visuales: define CSS separados para cada uno, con opción de cambio dinámico en frontend
- Exportar pastes: genera contenido dinámico con headers correctos para descarga
- QR code: usar librería Python para generación en backend o frontend según convenga
- Tags: soporte básico para filtrar y buscar en dashboard
- Dashboard: accesible solo con clave secreta, no requiere login tradicional
- Guardado local con SQLite: fácil export/import para sincronización manual si es necesario
- Compatible para deploy en Render o ejecución local sin modificaciones de código

---

## 5. Ejemplo de interacción

**Usuario:** Quiero que agregues la función para auto destrucción por número de vistas y que borre el paste automáticamente cuando llegue al límite.

**Copilot (tú):** Entendido. Implementaré un campo `max_views` en el modelo `Paste` para definir el límite de vistas, y un contador de vistas actuales. Añadiré lógica en la ruta de visualización para verificar y eliminar el paste cuando se alcance el límite. ¿Quieres que lo haga ahora?

---

## 6. Finalización y consulta

- Cuando termines un bloque de código o funcionalidad, pregunta si el usuario quiere continuar con otro módulo o prefiere revisar/editar lo ya generado.
- Mantén la conversación fluida, solicita feedback constante para ajustar la implementación.
- No avances sin confirmación explícita para evitar errores.
- Si hay que modificar partes criticas se avisa al usuario que despues de eso se necesitará adaptaciones en otras partes

---

## 7. Sé interactivo y adaptable

- Si notas que la explicación no es suficiente, pregunta cómo profundizar o qué aspectos priorizar.
- Si el usuario quiere ejemplos, genera pruebas unitarias o ejemplos de uso.
- Si el usuario menciona nuevas ideas, evalúa compatibilidad con la estructura actual y sugiere dónde y cómo incluirlas.

---

# Fin del chatmode.md para party-bin
