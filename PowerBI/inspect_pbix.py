import zipfile
import json
import os

pbix_path = r'PowerBI\Amazon_Ecommerce_Analytics_Dashboard.pbix'

with zipfile.ZipFile(pbix_path, 'r') as z:
    # 1. Read pages.json
    pages_json_str = z.read('Report/definition/pages/pages.json').decode('utf-8')
    pages_data = json.loads(pages_json_str)
    print("=== PAGES LIST ===")
    print(json.dumps(pages_data, indent=2))
    
    # 2. Iterate through each page directory
    page_order = pages_data.get('pageOrder', [])
    for p_id in page_order:
        page_path = f"Report/definition/pages/{p_id}/page.json"
        if page_path in z.namelist():
            p_json = json.loads(z.read(page_path).decode('utf-8'))
            print(f"\n================================================================================")
            print(f"PAGE: {p_json.get('displayName')} (ID: {p_id})")
            print(f"Dimensions: {p_json.get('width')}x{p_json.get('height')}")
            print(f"================================================================================")
            
            # Find all visuals in this page directory
            visual_prefix = f"Report/definition/pages/{p_id}/visuals/"
            visual_files = [f for f in z.namelist() if f.startswith(visual_prefix) and f.endswith('/visual.json')]
            print(f"Total Visuals: {len(visual_files)}")
            
            for v_file in visual_files:
                v_data = json.loads(z.read(v_file).decode('utf-8'))
                vis_obj = v_data.get('visual', {})
                vis_type = vis_obj.get('visualType')
                
                # Visual position
                pos = vis_obj.get('position', {})
                
                # Query projection / fields
                query = vis_obj.get('query', {})
                projections = query.get('queryState', {})
                
                # Visual objects (like title)
                objects = vis_obj.get('objects', {})
                title = "N/A"
                if 'title' in objects:
                    for item in objects['title']:
                        props = item.get('properties', {})
                        if 'text' in props:
                            expr = props['text'].get('expr', {})
                            title = expr.get('Literal', {}).get('Value', 'N/A')
                
                print(f"\n  --- Visual: {vis_type} ---")
                print(f"  Title: {title}")
                print(f"  Position: x={pos.get('x')}, y={pos.get('y')}, w={pos.get('width')}, h={pos.get('height')}, z={pos.get('z')}")
                print(f"  Full Visual JSON:")
                print(json.dumps(v_data, indent=4))
