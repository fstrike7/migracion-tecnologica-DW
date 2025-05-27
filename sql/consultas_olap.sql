-- ========================================
-- 1. ¿Qué celdas concentran más dispositivos conectados por hora?
-- ========================================
SELECT 
    dt.fecha,
    dt.hora,
    dc.id_celda,
    du.comuna,
    COUNT(fud.id_dispositivo) AS total_conexiones
FROM fact_uso_dispositivos fud
JOIN dim_tiempo dt ON fud.id_tiempo = dt.id_tiempo
JOIN dim_celda dc ON fud.id_celda = dc.id_celda
JOIN dim_ubicacion du ON dc.id_ubicacion = du.id_ubicacion
GROUP BY dt.fecha, dt.hora, dc.id_celda, du.comuna
ORDER BY total_conexiones DESC
LIMIT 10;

-- ========================================
-- 2. ¿Cuáles son las comunas con mayor uso de tecnología 2G?
-- ========================================
SELECT 
    du.comuna,
    dt.mes,
    dt.anio,
    COUNT(*) FILTER (WHERE dtg.tipo_red = '2G') AS conexiones_2g,
    COUNT(*) AS total_conexiones,
    ROUND(COUNT(*) FILTER (WHERE dtg.tipo_red = '2G') * 100.0 / COUNT(*), 2) AS porcentaje_2g
FROM fact_uso_dispositivos fud
JOIN dim_tiempo dt ON fud.id_tiempo = dt.id_tiempo
JOIN dim_tecnologia dtg ON fud.id_tecnologia = dtg.id_tecnologia
JOIN dim_celda dc ON fud.id_celda = dc.id_celda
JOIN dim_ubicacion du ON dc.id_ubicacion = du.id_ubicacion
GROUP BY du.comuna, dt.mes, dt.anio
ORDER BY porcentaje_2g DESC;

-- ========================================
-- 3. ¿Dónde se concentran más reclamos de red?
-- ========================================
SELECT 
    du.comuna,
    dt.fecha,
    SUM(fsc.errores) AS total_errores,
    SUM(fsc.caidas) AS total_caidas
FROM fact_status_conexion fsc
JOIN dim_tiempo dt ON fsc.id_tiempo = dt.id_tiempo
JOIN dim_celda dc ON fsc.id_celda = dc.id_celda
JOIN dim_ubicacion du ON dc.id_ubicacion = du.id_ubicacion
GROUP BY du.comuna, dt.fecha
ORDER BY total_errores DESC
LIMIT 10;

-- ========================================
-- 4. ¿Qué porcentaje de tiempo pasan ciertos dispositivos conectados a la misma celda?
-- ========================================
SELECT 
    id_dispositivo,
    id_celda,
    COUNT(*) AS horas_conectado,
    ROUND(COUNT(*) * 100.0 / 24, 2) AS porcentaje_diario
FROM fact_uso_dispositivos
GROUP BY id_dispositivo, id_celda
HAVING COUNT(*) >= 12  -- más de 12 horas/día
ORDER BY porcentaje_diario DESC;

-- ========================================
-- 5. ¿Qué comunas tienen peor relación infraestructura/uso? (infraestructura saturada)
-- ========================================
SELECT 
    du.comuna,
    COUNT(DISTINCT fud.id_dispositivo) AS dispositivos,
    SUM(fsc.caidas) AS caidas_reportadas,
    SUM(fsc.errores) AS errores_reportados
FROM fact_uso_dispositivos fud
JOIN dim_celda dc ON fud.id_celda = dc.id_celda
JOIN dim_ubicacion du ON dc.id_ubicacion = du.id_ubicacion
LEFT JOIN fact_status_conexion fsc ON dc.id_celda = fsc.id_celda AND fud.id_tiempo = fsc.id_tiempo
GROUP BY du.comuna
ORDER BY dispositivos DESC, caidas_reportadas DESC;

-- ========================================
-- 6. Evolución temporal del uso de 4G vs 2G en una comuna
-- ========================================
SELECT 
    dt.fecha,
    dtg.tipo_red,
    COUNT(*) AS conexiones
FROM fact_uso_dispositivos fud
JOIN dim_tiempo dt ON fud.id_tiempo = dt.id_tiempo
JOIN dim_tecnologia dtg ON fud.id_tecnologia = dtg.id_tecnologia
JOIN dim_celda dc ON fud.id_celda = dc.id_celda
JOIN dim_ubicacion du ON dc.id_ubicacion = du.id_ubicacion
WHERE du.comuna = 'PALERMO'
  AND dtg.tipo_red IN ('2G', '4G')
GROUP BY dt.fecha, dtg.tipo_red
ORDER BY dt.fecha, dtg.tipo_red;
