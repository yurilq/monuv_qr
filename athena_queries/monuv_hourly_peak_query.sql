--Quais clientes mais consomem a solução?

SELECT ClientCode, COUNT(*) as TotalScans
FROM monuv_qr_table
GROUP BY ClientCode
ORDER BY TotalScans DESC;

--Existem horários de pico na operação das salas de cinema?

SELECT hour(Timestamp) as Hour, COUNT(*) as TotalScans
FROM monuv_qr_table
GROUP BY hour(Timestamp)
ORDER BY TotalScans DESC;


--Existe uma sazonalidade nessa operação?

SELECT month(FormattedDate) as Month, COUNT(*) as TotalScans
FROM monuv_qr_table
GROUP BY month(FormattedDate)
ORDER BY TotalScans DESC;


--Quais são as cidades com as salas mais movimentadas?

SELECT City, COUNT(*) as TotalScans
FROM monuv_qr_table
GROUP BY City
ORDER BY TotalScans DESC;


--Existem QR Codes com conteúdo repetido, sendo fraudados ou sendo utilizados múltiplas vezes em locais e/ou horários diferentes?

SELECT QrContent, COUNT(*) as ScanCount, MIN(Timestamp) as FirstScan, MAX(Timestamp) as LastScan
FROM monuv_qr_table
GROUP BY QrContent
HAVING ScanCount > 1
ORDER BY ScanCount DESC;
