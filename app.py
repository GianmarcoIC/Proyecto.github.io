from flask import Flask, render_template, request, redirect, url_for, flash
app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Necesario para mostrar mensajes flash

VALID_CATEGORIES = ['Chocolates', 'Caramelos', 'Mashmelos', 'Galletas', 'Salados', 'Gomas de mascar']

@app.route('/', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        # Obtener datos del formulario
        product_name = request.form.get('product_name')
        product_price = request.form.get('product_price')
        product_categories = request.form.getlist('product_categories')
        product_on_sale = request.form.get('product_on_sale')

        # Validaciones
        errors = []
        if not product_name or len(product_name) > 20:
            errors.append("El nombre del producto no debe ser mayor a 20 caracteres.")
        
        try:
            product_price = float(product_price)
            if not (0 < product_price < 999):
                errors.append("El precio del producto debe ser mayor a 0 y menor a 999 soles.")
        except ValueError:
            errors.append("Por favor verifique el campo del precio.")
        
        for category in product_categories:
            if category not in VALID_CATEGORIES:
                errors.append(f"La categoría {category} no es válida.")
                break
        
        if product_on_sale not in ['Si', 'No']:
            errors.append("El estado del producto en venta no es válido.")
        
        # Mostrar resultados
        if errors:
            for error in errors:
                flash(error, 'danger')
            flash("Lo sentimos no pudo crear este producto.", 'danger')
        else:
            flash("Felicidades su producto se agregó.", 'success')

        return redirect(url_for('form'))
    
    return render_template('form.html', categories=VALID_CATEGORIES)

if __name__ == '__main__':
    app.run(debug=True)
