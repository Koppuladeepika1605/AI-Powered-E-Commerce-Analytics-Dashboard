import zipfile
import json
import os

pbix_path = r'PowerBI\Amazon_Ecommerce_Analytics_Dashboard.pbix'

with zipfile.ZipFile(pbix_path, 'r') as z:
    pages_json_str = z.read('Report/definition/pages/pages.json').decode('utf-8')
    pages_data = json.loads(pages_json_str)
    
    summary = []
    
    page_order = pages_data.get('pageOrder', [])
    for p_idx, p_id in enumerate(page_order):
        page_path = f"Report/definition/pages/{p_id}/page.json"
        p_json = json.loads(z.read(page_path).decode('utf-8'))
        page_displayName = p_json.get('displayName')
        
        page_info = {
            "page_number": p_idx + 1,
            "id": p_id,
            "displayName": page_displayName,
            "width": p_json.get('width'),
            "height": p_json.get('height'),
            "visuals": []
        }
        
        visual_prefix = f"Report/definition/pages/{p_id}/visuals/"
        visual_files = [f for f in z.namelist() if f.startswith(visual_prefix) and f.endswith('/visual.json')]
        
        for v_file in visual_files:
            v_data = json.loads(z.read(v_file).decode('utf-8'))
            vis = v_data.get('visual', {})
            vis_type = vis.get('visualType')
            pos = vis.get('position', {})
            
            # Extract visual title
            title = None
            objects = vis.get('objects', {})
            if 'title' in objects:
                for item in objects['title']:
                    props = item.get('properties', {})
                    if 'text' in props:
                        expr = props['text'].get('expr', {})
                        title = expr.get('Literal', {}).get('Value', '').strip("'\"")
            
            # Query state / projections
            query = vis.get('query', {})
            q_state = query.get('queryState', {})
            
            fields_by_role = {}
            for role, role_data in q_state.items():
                projections = role_data.get('projections', [])
                fields = []
                for p in projections:
                    query_ref = p.get('queryRef', '')
                    # try to see property or measure name
                    field_expr = p.get('field', {})
                    if 'Measure' in field_expr:
                        m_prop = field_expr['Measure'].get('Property', '')
                        fields.append(f"Measure({m_prop})")
                    elif 'Column' in field_expr:
                        c_prop = field_expr['Column'].get('Property', '')
                        fields.append(f"Column({c_prop})")
                    elif 'HierarchyLevel' in field_expr:
                        h_prop = field_expr['HierarchyLevel'].get('Level', '')
                        fields.append(f"HierarchyLevel({h_prop})")
                    else:
                        fields.append(query_ref)
                fields_by_role[role] = fields
                
            page_info["visuals"].append({
                "type": vis_type,
                "title": title,
                "position": pos,
                "fields": fields_by_role,
                "raw_query_state": q_state
            })
        summary.append(page_info)

with open(r'PowerBI\pbix_summary.json', 'w') as f:
    json.dump(summary, f, indent=2)

for page in summary:
    print(f"\n=======================================================")
    print(f"PAGE {page['page_number']}: {page['displayName']}")
    print(f"=======================================================")
    for idx, v in enumerate(page['visuals']):
        print(f"Visual {idx+1}: [{v['type']}] Title: '{v['title']}'")
        print(f"   Fields: {v['fields']}")
        print(f"   Position: x={v['position'].get('x')}, y={v['position'].get('y')}, w={v['position'].get('width')}, h={v['position'].get('height')}")
