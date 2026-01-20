import json
import os

def process_inventory():
    try:
        with open('inventory_clean.json', 'r') as f:
            data = json.load(f)
        
        # Headers: ["Item ID", "Item Name", "SKU", "Description", "Rate", "Account", "Account Code", "Tax Name", "Tax Percentage", "Tax Type", "Purchase Tax Name", "Purchase Tax Percentage", "Purchase Tax Type", "Product Type", "Source", "Reference ID", "Last Sync Time", "Status", ...]
        # Status is index 17
        active_items = []
        for row in data[1:]: # Skip header
            if len(row) > 17 and row[17] == 'Active':
                name = row[1]
                desc = row[3]
                price = row[4]
                
                # Basic Categorization based on name
                cat = 'general'
                n = name.lower()
                if 'router' in n or 'switch' in n or 'cpe' in n or 'nanostation' in n or 'rocket' in n or 'ubiquiti' in n or 'tp-link' in n:
                    cat = 'networking'
                elif 'camera' in n or 'nvr' in n or 'dvr' in n or 'security' in n or 'sunell' in n:
                    cat = 'security'
                elif 'cable' in n or 'connector' in n or 'rj45' in n or 'trunking' in n or 'ups' in n or 'adapter' in n or 'toner' in n:
                    cat = 'accessories'
                
                # Assign Icon
                icon = 'package'
                if cat == 'networking': icon = 'wifi'
                if cat == 'security': icon = 'shield'
                if cat == 'accessories': icon = 'zap'
                if 'cable' in n: icon = 'cable'
                if 'camera' in n: icon = 'camera'
                if 'router' in n: icon = 'router'
                if 'server' in n: icon = 'server'
                if 'hard drive' in n or 'storage' in n: icon = 'hard-drive'

                # Clean price (remove USD)
                price_clean = price.replace('USD ', '$')
                
                active_items.append({
                    'id': row[0],
                    'name': name,
                    'desc': desc if desc else name,
                    'price': price_clean,
                    'cat': cat,
                    'icon': icon,
                    'img': 'https://images.unsplash.com/photo-1544244015-0cd4b3ffecf2?w=600'
                })
        
        # Save to JS file
        js_content = f"window.inventoryData = {json.dumps(active_items, indent=4)};"
        with open('js/inventory.js', 'w') as f:
            f.write(js_content)
        print(f"Processed {len(active_items)} active items.")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if not os.path.exists('js'):
        os.makedirs('js')
    process_inventory()
