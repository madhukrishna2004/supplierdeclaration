import pandas as pd

# Load CSV only once
df = pd.read_csv("global-uk-tariff.csv", encoding="ISO-8859-1")

# Normalize all codes as strings and strip spaces
df["commodity"] = df["commodity"].astype(str).str.strip()

def lookup_commodity_details(commodity_code):
    try:
        code = str(commodity_code).strip()
        original_code = code
        print(f"\n🔍 Incoming Lookup Code: {code}")
        print(f"📊 Columns in DataFrame: {list(df.columns)}")

        # Try exact match
        row = df[df["commodity"] == code]
        if not row.empty:
            print(f"✅ Exact match found: {code}")
        else:
            # Try trimming trailing zeroes
            while code.endswith("0") and len(code) > 6:
                code = code[:-1]
                print(f"🔁 Trying trimmed code: {code}")
                row = df[df["commodity"] == code]
                if not row.empty:
                    print(f"✅ Match found after trimming: {code}")
                    break

        # Try 8-digit fallback
        if row.empty and len(original_code) >= 8:
            code8 = original_code[:8]
            print(f"🔁 Trying 8-digit fallback: {code8}")
            row = df[df["commodity"] == code8]
            if not row.empty:
                print(f"✅ Match found on 8-digit fallback: {code8}")

        if row.empty:
            print("❌ No match found at all.")
            return {
                "short_code": original_code[:4],
                "heading": "N/A",
                "hmrc_description": "N/A",
                "duty": "N/A"
            }

        row_data = row.iloc[0].to_dict()
        print(f"\n📦 Matched Row Data:")
        for k, v in row_data.items():
            print(f"  - {k}: {v}")

        # Access fields explicitly
        heading = str(row_data.get("description", "N/A")).strip()
        hmrc_description = str(row_data.get("Product-specific rule of origin", "N/A")).strip()
        duty = str(row_data.get("ukgt_duty_rate", "N/A")).strip()

        print("\n🔎 Extracted Fields:")
        print(f"  📌 Heading: {heading}")
        print(f"  📌 HMRC Description: {hmrc_description}")
        print(f"  📌 UKGT Duty Rate: {duty}")

        return {
            "short_code": original_code[:4],
            "heading": heading,
            "hmrc_description": hmrc_description,
            "duty": duty
        }

    except Exception as e:
        print("❌ Exception occurred during lookup:", e)
        return {
            "short_code": str(commodity_code)[:4],
            "heading": "N/A",
            "hmrc_description": "N/A",
            "duty": "N/A"
        }
