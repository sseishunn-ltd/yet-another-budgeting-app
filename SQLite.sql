-- SQLite
SELECT
   a.transaction_id, a.created_at, a.from_id, c.account_name, a.to_id, d.account_name, a.category_id, b.category_name, a.amount, a.comment
FROM
   transactions_EUR as a
LEFT JOIN categories as b ON a.category_id = b.category_id
LEFT JOIN accounts as c ON a.from_id = c.account_id
LEFT JOIN accounts as d ON a.to_id = d.account_id
ORDER BY
   a.transaction_id;

INSERT INTO accounts
VALUES (14, "Beertija", 1, 1, 1);

SELECT * from (
SELECT * from transactions_EUR ORDER BY transaction_id DESC LIMIT 5)
ORDER BY transaction_id ASC;

SELECT * FROM (
   SELECT datetime(a.created_at, 'unixepoch') as datetime, 
      b.category_name,
      CAST(a.amount AS FLOAT) as amount,
      c.account_name as acc_from,
      d.account_name acc_to, 
      a.comment
   FROM
      transactions_EUR as a
      LEFT JOIN categories as b ON a.category_id = b.category_id
      LEFT JOIN accounts as c ON a.from_id = c.account_id
      LEFT JOIN accounts as d ON a.to_id = d.account_id
   ORDER BY
      a.transaction_id
   DESC LIMIT 10)
   ORDER BY
      datetime ASC;


SELECT * FROM (
      SELECT a.transaction_id,
         datetime(a.created_at, 'unixepoch') as datetime, 
         b.category_name,
         CAST(a.amount AS FLOAT) as amount,
         c.account_name as acc_from,
         d.account_name acc_to, 
         a.comment
      FROM
         transactions_EUR as a
         LEFT JOIN categories as b ON a.category_id = b.category_id
         LEFT JOIN accounts as c ON a.from_id = c.account_id
         LEFT JOIN accounts as d ON a.to_id = d.account_id
      ORDER BY
         a.transaction_id
      DESC LIMIT 5
ORDER BY
      datetime ASC;