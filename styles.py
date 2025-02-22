def get_css():
    """Retorna o CSS para estilização da interface."""
    return """
        <style>
            body {
                background-color: #121212;
                color: white;
                font-family: Arial, sans-serif;
            }
            .centered-buttons {
                display: flex;
                flex-direction: column;
                align-items: center;
                gap: 20px;
                justify-content: center;
                height: 100vh;
            }
            .custom-button {
                width: 280px;
                height: 65px;
                font-size: 20px;
                font-weight: bold;
                background: linear-gradient(135deg, #6a11cb, #2575fc);
                color: white;
                border: none;
                border-radius: 12px;
                box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
                transition: all 0.3s ease;
                cursor: pointer;
            }
            .custom-button:hover {
                background: linear-gradient(135deg, #2575fc, #6a11cb);
                transform: scale(1.05);
            }
            .custom-button:active {
                transform: scale(0.95);
            }
        </style>
    """