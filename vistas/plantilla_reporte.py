import base64

def generar_html_reporte(nombre, dni, fecha_eval, html_ariscat, html_torrington, lista_sugerencias_html, otros_comentarios):
    return f"""
    <div style="font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; border: 2px solid #4f8bf9; padding: 20px; border-radius: 10px; background-color: white; color: black;">
        <h3 style="text-align: center; margin-top: 0; color: #1e3d59;">Evaluación Neumonológica Prequirúrgica</h3>
        <hr style="border-top: 2px solid #4f8bf9;">
        <p><strong>Paciente:</strong> {nombre if nombre else '_________________________'} &nbsp;&nbsp;&nbsp; <strong>DNI/HC:</strong> {dni if dni else '________________'}</p>
        <p><strong>Fecha:</strong> {fecha_eval}</p>
        <br>
        {html_ariscat}
        {html_torrington}
        <p><strong><u>SUGERENCIAS E INDICACIONES:</u></strong></p>
        <ul>{lista_sugerencias_html}</ul>
        <p><strong>Observaciones:</strong> {otros_comentarios if otros_comentarios else 'Ninguna.'}</p>
        <br><br><br>
        <p style="text-align: right;"><em>Firma y Sello del Profesional: ___________________________</em></p>
    </div>
    """

def generar_boton_impresion(html_reporte):
    b64_html = base64.b64encode(html_reporte.encode('utf-8')).decode('utf-8')
    return f"""
    <script>
    function imprimirLimpio() {{
        const b64 = "{b64_html}";
        const decoded_html = decodeURIComponent(escape(window.atob(b64)));
        const ventana = window.open('', '_blank');
        ventana.document.write('<html><head><title>Reporte Médico</title></head><body>');
        ventana.document.write(decoded_html);
        ventana.document.write('</body></html>');
        ventana.document.close();
        setTimeout(function() {{
            ventana.print();
            ventana.close();
        }}, 250);
    }}
    </script>
    <div style="display: flex; justify-content: center; margin-top: 20px;">
        <button onclick="imprimirLimpio()" style="background-color: #4f8bf9; color: white; padding: 12px 24px; border: none; border-radius: 8px; font-size: 16px; font-weight: bold; cursor: pointer; box-shadow: 0 4px 6px rgba(0,0,0,0.1); width: 100%; max-width: 400px;">
        🖨️ Imprimir / Guardar PDF (Versión Limpia)
        </button>
    </div>
    """
