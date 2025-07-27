import re

# Open the MySQL dump file and a new file for PostgreSQL
with open("madhuuu.sql", "r", encoding="utf-8") as infile, open("postgres_dump.sql", "w", encoding="utf-8") as outfile:
    for line in infile:
        # Convert MySQL AUTO_INCREMENT to PostgreSQL SERIAL
        line = re.sub(r'AUTO_INCREMENT', 'SERIAL', line)
        
        # Convert backticks (`table_name`) to double quotes ("table_name")
        line = re.sub(r'`', '"', line)

        # Remove MySQL-specific "ENGINE=InnoDB"
        line = re.sub(r'ENGINE=InnoDB', '', line)

        # Remove MySQL "UNSIGNED" type (PostgreSQL does not support it)
        line = re.sub(r'UNSIGNED', '', line)

        # Change "utf8mb4" to "UTF8" (PostgreSQL standard)
        line = re.sub(r'utf8mb4', 'UTF8', line)

        # Remove "COMMENT" lines (not supported in PostgreSQL)
        line = re.sub(r'COMMENT .*?,', ',', line)

        # Convert "TINYINT(1)" to "BOOLEAN" in PostgreSQL
        line = re.sub(r'TINYINT\(1\)', 'BOOLEAN', line)

        # Convert "DATETIME" to "TIMESTAMP"
        line = re.sub(r'DATETIME', 'TIMESTAMP', line)

        outfile.write(line)

print("✅ Conversion complete! The file 'postgres_dump.sql' is ready for import.")
