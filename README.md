# Optimización del uso de red móvil y migración tecnológica en CABA

## Índice

1. [Contexto](#contexto)  
2. [Definición del problema](#definición-del-problema)  
3. [Objetivo principal](#objetivo-principal)  
4. [Objetivos secundarios](#objetivos-secundarios)  
5. [Preguntas planteadas](#preguntas-planteadas)  
   - [Identificación de zonas críticas](#identificación-de-zonas-críticas)  
   - [Caracterización de usuarios no migrados](#caracterización-de-usuarios-no-migrados)  
   - [Impacto de la migración](#impacto-de-la-migración)  
6. [Modelo conceptual](#modelo-conceptual)  
7. [Modelo lógico](#modelo-lógico)
8. [Instalación y ejecución](#instalación-y-ejecución)

---

## Contexto

La red móvil en la Ciudad Autónoma de Buenos Aires está en constante transformación tecnológica. En los últimos años, los operadores comenzaron el apagado progresivo de las redes 2G, obligando a los usuarios a migrar a tecnologías más modernas (4G y 5G).

Sin embargo, aún existe un número considerable de personas que continúan utilizando dispositivos y planes obsoletos. Esta situación genera cuellos de botella en zonas críticas, baja calidad de servicio y dificulta la gestión eficiente de los recursos de red. Al mismo tiempo, se abren oportunidades para ofrecer beneficios personalizados que aceleren la migración tecnológica y mejoren la experiencia de uso.

La información para este análisis puede obtenerse parcialmente de fuentes abiertas como ENACOM, INDEC, portales de datos abiertos (Buenos Aires Data, datos.gob.ar) y operadores de red móvil.

## Definición del problema

La coexistencia de redes móviles obsoletas (2G) con redes modernas (4G/5G) genera ineficiencias técnicas, saturación en zonas de alta densidad de usuarios y un uso inadecuado de los recursos de red. A esto se suma una baja adopción tecnológica en ciertos perfiles de usuarios, producto de barreras económicas, técnicas o de desconocimiento.

## Objetivo principal

Acelerar la migración de usuarios de redes 2G hacia redes 4G/5G en zonas críticas de la Ciudad de Buenos Aires, mejorando la eficiencia del servicio móvil mediante acciones basadas en analítica multidimensional y beneficios personalizados.

## Objetivos secundarios

- Identificar comunas de la Ciudad de Buenos Aires donde más del 60% de las conexiones móviles activas se realizan a través de redes 2G (consideradas tecnologías obsoletas), utilizando datos por tecnología y zona.
- Evaluar el impacto de la migración en el uso de red y calidad del servicio.

## Preguntas planteadas

### Identificación de zonas críticas

- ¿Qué porcentaje de conexiones por comuna/barrio se realiza en redes 2G?  
- ¿Cómo se distribuyen las antenas por tipo de red (2G, 4G, 5G) y proveedor en CABA?

### Caracterización de usuarios no migrados

- ¿Qué porcentaje de dispositivos conectados a redes 2G no son compatibles con redes LTE (4G) o 5G, por comuna?

### Impacto de la migración

- Cliente que, tras comenzar a utilizar redes 4G o 5G, no volvió a conectarse a redes 2G en un período posterior de análisis.  
- ¿Cuántos clientes quedaron sin posibilidad de conexión debido al uso de dispositivos obsoletos?  
- ¿Cómo evolucionó la tasa de fallas en la conexión de las celdas antes y luego de la migración?  
- ¿En qué franjas horarias se registra mayor saturación de red, en comparación con el promedio de uso, en zonas donde coexisten antenas 2G y 4G?

## Modelo conceptual

El modelo conceptual está diseñado bajo un enfoque multidimensional con:

### Tablas de hechos

- **Fact_StatusConexion**  
  Registra eventos relacionados con la calidad de la conexión entre celdas, agregados en una unidad temporal determinada (por ejemplo: hora, día).

- **Fact_UsoDispositivos**  
  Registra eventos de conexión entre un dispositivo y una celda, identificando el momento exacto y la zona geográfica en la que ocurrió.

![Logico y conceptual-Page-1 drawio](https://github.com/user-attachments/assets/1fc86d32-ead6-4e1a-967d-8d88b19eef92)

### Dimensiones jerárquicas

- **Ubicación** → Ciudad → Comuna → Barrio → Celda  
- **Tiempo** → Día → Semana → Mes → Trimestre → Año  
- **Dispositivo** → Modelo → Marca → Gama

## Modelo lógico

Este modelo representa un data warehouse centrado en el análisis de dispositivos móviles, su cobertura y los registros de uso, con dimensiones normalizadas jerárquicamente para una mayor organización y eficiencia de almacenamiento.

![Logico y conceptual-Page-2 drawio](https://github.com/user-attachments/assets/41429bfe-fab4-4bf9-bc03-82525c225ffe)

## Instalación y ejecución

Guía de instalación para ejecutar este proyecto localmente en [docs/INSTALACION.md](docs/INSTALACION.md)
