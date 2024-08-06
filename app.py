from flask import Flask, render_template, request, redirect, url_for, send_file, flash
import pandas as pd
from io import BytesIO
import os

# Importar las configuraciones y las funciones de la base de datos
from db import get_all_items, get_item_by_id, create_item, update_item, delete_item, get_paginated_items, get_total_items_count, log_file_upload, get_all_file_uploads, delete_file_upload

app = Flask(__name__)
app.secret_key = 'supersecretkey'

@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    per_page = 5
    items = get_paginated_items(page, per_page)
    total_items = get_total_items_count()
    total_pages = (total_items + per_page - 1) // per_page
    return render_template('read.html', items=items, page=page, total_pages=total_pages)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        quantity = request.form['quantity']
        
        create_item(name, description, price, quantity)
        return redirect(url_for('index'))
    return render_template('create.html')

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    item = get_item_by_id(id)
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        quantity = request.form['quantity']
        
        update_item(id, name, description, price, quantity)
        return redirect(url_for('index'))
    return render_template('update.html', item=item)

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    delete_item(id)
    return redirect(url_for('index'))

@app.route('/download_report')
def download_report():
    items = get_all_items()
    data = []
    for item in items:
        data.append({
            "ID": item[0],
            "Producto": item[1],
            "Descripción": item[2],
            "Precio": item[3],
            "Cantidad": item[4]
        })

    df = pd.DataFrame(data)
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='openpyxl')
    df.to_excel(writer, index=False, sheet_name='Productos')
    writer.close()
    output.seek(0)
    
    return send_file(output, download_name="reporte_productos.xlsx", as_attachment=True)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file and file.filename.endswith('.xlsx'):
            # Crear el directorio 'uploads' si no existe
            if not os.path.exists('uploads'):
                os.makedirs('uploads')

            filepath = os.path.join('uploads', file.filename)
            file.save(filepath)
            
            df = pd.read_excel(filepath)
            
            # Verificar que las columnas necesarias existan en el DataFrame
            expected_columns = ['Producto', 'Descripción', 'Precio', 'Cantidad']
            if not all(column in df.columns for column in expected_columns):
                flash('El archivo Excel no tiene las columnas requeridas: Producto, Descripción, Precio, Cantidad', 'danger')
                return redirect(url_for('upload'))
            
            for _, row in df.iterrows():
                try:
                    create_item(row['Producto'], row['Descripción'], row['Precio'], row['Cantidad'])
                except KeyError as e:
                    flash(f'Error en la fila {_ + 1}: {e}', 'danger')
                    return redirect(url_for('upload'))
                
            total_loaded = len(df)
            log_file_upload(file.filename, total_loaded)
            flash(f'{total_loaded} productos cargados exitosamente.', 'success')
            return redirect(url_for('index'))
        else:
            flash('Por favor, sube un archivo Excel válido.', 'danger')
    uploads = get_all_file_uploads()
    return render_template('upload.html', uploads=uploads)

@app.route('/delete_upload/<int:id>', methods=['POST'])
def delete_upload(id):
    delete_file_upload(id)
    flash('El registro de carga ha sido eliminado.', 'success')
    return redirect(url_for('upload'))

if __name__ == '__main__':
    app.run(debug=True)