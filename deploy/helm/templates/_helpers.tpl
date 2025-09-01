{{/*
Expand the name of the chart.
*/}}
{{- define "educational-chatbot.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
*/}}
{{- define "educational-chatbot.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "educational-chatbot.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "educational-chatbot.labels" -}}
helm.sh/chart: {{ include "educational-chatbot.chart" . }}
{{ include "educational-chatbot.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
app.kubernetes.io/component: chatbot
app.kubernetes.io/part-of: educational-platform
{{- end }}

{{/*
Selector labels
*/}}
{{- define "educational-chatbot.selectorLabels" -}}
app.kubernetes.io/name: {{ include "educational-chatbot.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Frontend specific labels
*/}}
{{- define "educational-chatbot.frontend.labels" -}}
{{ include "educational-chatbot.labels" . }}
app.kubernetes.io/component: frontend
{{- end }}

{{/*
Frontend selector labels
*/}}
{{- define "educational-chatbot.frontend.selectorLabels" -}}
{{ include "educational-chatbot.selectorLabels" . }}
app.kubernetes.io/component: frontend
{{- end }}

{{/*
Backend specific labels
*/}}
{{- define "educational-chatbot.backend.labels" -}}
{{ include "educational-chatbot.labels" . }}
app.kubernetes.io/component: backend
{{- end }}

{{/*
Backend selector labels
*/}}
{{- define "educational-chatbot.backend.selectorLabels" -}}
{{ include "educational-chatbot.selectorLabels" . }}
app.kubernetes.io/component: backend
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "educational-chatbot.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "educational-chatbot.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}

{{/*
Frontend fullname
*/}}
{{- define "educational-chatbot.frontend.fullname" -}}
{{- printf "%s-%s" (include "educational-chatbot.fullname" .) "frontend" }}
{{- end }}

{{/*
Backend fullname
*/}}
{{- define "educational-chatbot.backend.fullname" -}}
{{- printf "%s-%s" (include "educational-chatbot.fullname" .) "backend" }}
{{- end }}

{{/*
Storage name
*/}}
{{- define "educational-chatbot.storage.name" -}}
{{- printf "%s-%s" (include "educational-chatbot.fullname" .) "storage" }}
{{- end }}

{{/*
ConfigMap name
*/}}
{{- define "educational-chatbot.configmap.name" -}}
{{- printf "%s-%s" (include "educational-chatbot.fullname" .) "config" }}
{{- end }}
