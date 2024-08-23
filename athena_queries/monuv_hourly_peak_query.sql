SELECT 
    hour(Timestamp) as Hour, 
    COUNT(*) as TotalScans 
FROM monuv_qr_table 
GROUP BY hour(Timestamp) 
ORDER BY TotalScans DESC
