SELECT
    '$' || ROUND(SUM(oeadc.amount_cents) / 100.0, 2)::TEXT as total_amount_dollars,
    oeadc.merchant_name
FROM OrganizationEmployeeAccountDebitCardTransaction oeadc
GROUP BY oeadc.merchant_name
ORDER BY SUM(oeadc.amount_cents) DESC;