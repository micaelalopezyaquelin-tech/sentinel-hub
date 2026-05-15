from flask import Flask, request, render_template_string
import os

app = Flask(__name__)

# Las misiones y juegos se quedan exactamente igual con tu diseño Cyberpunk
PAGINA_NUEVA = """
<html>
    <head>
        <title>Sentinel Cyber Hub 🛰️</title>
        <meta name='viewport' content='width=device-width, initial-scale=1.0'>
        <style>
            :root {
                --bg: #07050d;
                --panel: rgba(10, 8, 20, 0.88);
                --border-dim: rgba(255, 255, 255, 0.04);
                --green-neon: #50fa7b;
                --green-glow: rgba(80, 250, 123, 0.4);
                --cyan-neon: #8be9fd;
                --magenta-neon: #ff79c6;
                --yellow-neon: #f1fa8c;
            }

            body {
                background-color: var(--bg);
                color: #ffffff;
                font-family: 'Courier New', Courier, monospace;
                margin: 0;
                padding: 10px 10px 40px 10px;
                display: flex;
                flex-direction: column;
                align-items: center;
                min-height: 100vh;
                box-sizing: border-box;
                overflow-x: hidden;
            }

            /* SPLASH SCREEN */
            #splash-screen {
                position: fixed;
                top: 0; left: 0;
                width: 100vw; height: 100vh;
                background-color: var(--bg);
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                z-index: 10000;
                transition: opacity 0.6s ease;
            }

            .logo-tactical-wrap {
                position: relative;
                width: 120px; height: 120px;
                display: flex; align-items: center; justify-content: center;
            }
            .logo-sun-s {
                width: 100px; height: 100px;
                background: linear-gradient(135deg, #100d1a, #07050d);
                border: 3px solid transparent;
                border-image: linear-gradient(135deg, var(--green-neon), var(--cyan-neon)) 1;
                border-radius: 50%;
                display: flex; align-items: center; justify-content: center;
                font-size: 3.5em; font-weight: 900;
                color: transparent; -webkit-background-clip: text; background-clip: text;
                background-image: linear-gradient(135deg, var(--green-neon), var(--cyan-neon));
                text-shadow: 0 0 15px rgba(80, 250, 123, 0.4);
                box-shadow: 0 0 45px rgba(80, 250, 123, 0.25);
                animation: pulseTactical 2.2s infinite ease-in-out;
            }
            @keyframes pulseTactical {
                0%, 100% { transform: scale(1); }
                50% { transform: scale(1.04); }
            }

            /* PANTALLAS DE ACCESO */
            .access-card {
                display: none;
                width: 100%;
                max-width: 440px;
                background: var(--panel);
                border: 1px solid var(--border-dim);
                box-shadow: 0 0 40px rgba(0, 0, 0, 0.7);
                border-radius: 12px;
                padding: 30px 25px;
                margin-top: 50px;
                box-sizing: border-box;
                text-align: center;
                animation: scaleInCompact 0.4s ease forwards;
            }

            .gate-warning {
                font-size: 0.85em;
                font-weight: bold;
                margin-bottom: 18px;
                letter-spacing: 2px;
                text-transform: uppercase;
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 8px;
            }

            .trivia-box {
                background: rgba(0, 0, 0, 0.6);
                border: 1px solid rgba(139, 233, 253, 0.1);
                padding: 18px;
                border-radius: 8px;
                margin-bottom: 25px;
                font-size: 0.9em;
                text-align: left;
                line-height: 1.5;
                color: #e0e0e0;
            }

            .options-grid { display: flex; flex-direction: column; gap: 12px; }

            .btn-option-gate {
                background: linear-gradient(135deg, #120f1f, #07050d);
                border: 1px solid rgba(139, 233, 253, 0.1);
                border-left: 3px solid var(--cyan-neon);
                color: #e0e0e0; padding: 16px; border-radius: 6px;
                font-family: inherit; font-weight: bold; cursor: pointer;
                transition: all 0.2s ease; text-align: left; font-size: 0.9em;
            }
            .btn-option-gate:hover { background: linear-gradient(135deg, #1a1529, #120f1f); color: #fff; }

            /* INTERFAZ PRINCIPAL */
            .main-content {
                display: none;
                opacity: 0;
                width: 100%;
                max-width: 480px;
                transition: opacity 0.6s ease;
            }

            .achievements-row { display: flex; justify-content: center; gap: 10px; margin-bottom: 15px; width: 100%; }
            .badge {
                background: rgba(0,0,0,0.6); border: 1px solid rgba(255,255,255,0.05);
                padding: 8px 12px; border-radius: 8px; font-size: 0.65em; color: #44475a;
                text-transform: uppercase; font-weight: bold; letter-spacing: 1px; display: flex; align-items: center; gap: 5px;
            }
            .badge.unlocked {
                border-color: var(--yellow-neon); color: var(--yellow-neon);
                box-shadow: 0 0 10px rgba(241, 250, 140, 0.15); background: rgba(241, 250, 140, 0.05);
            }

            .tabs-nav { display: flex; background: rgba(0, 0, 0, 0.75); border: 1px solid var(--border-dim); border-radius: 10px; padding: 3px; margin-bottom: 20px; gap: 3px; position: relative; }
            .tab-btn {
                flex: 1; background: transparent; border: none; color: #6272a4; padding: 15px 6px;
                font-family: inherit; font-size: 0.8em; font-weight: bold; border-radius: 7px; cursor: pointer;
                display: flex; align-items: center; justify-content: center; gap: 8px; text-transform: uppercase;
            }
            .tab-btn.active { background: linear-gradient(135deg, rgba(80, 250, 123, 0.1), rgba(80, 250, 123, 0.01)); color: #fff; border: 1px solid rgba(80, 250, 123, 0.3); }
            .tab-icon { width: 18px; height: 18px; fill: #6272a4; }
            .tab-btn.active .tab-icon { fill: #fff; }

            .window-box { display: none; background: var(--panel); border: 1px solid var(--border-dim); border-top: 1px solid var(--green-neon); border-radius: 14px; padding: 25px 22px; box-shadow: 0 0 50px rgba(0, 0, 0, 0.7); }
            .window-box.active { display: block; animation: scaleInCompact 0.4s ease forwards; }
            @keyframes scaleInCompact { from { opacity: 0; transform: scale(0.98); } to { opacity: 1; transform: scale(1); } }

            .window-header { font-size: 0.85em; color: var(--green-neon); font-weight: bold; border-bottom: 1px dashed rgba(80, 250, 123, 0.18); padding-bottom: 14px; margin-bottom: 20px; text-transform: uppercase; display: flex; align-items: center; gap: 10px; }
            .btn-action { background: linear-gradient(135deg, #120f1f, #07050d); border: 1px solid rgba(80, 250, 123, 0.18); color: var(--green-neon); padding: 15px; border-radius: 8px; cursor: pointer; font-family: inherit; font-weight: bold; width: 100%; text-transform: uppercase; font-size: 0.9em; margin-bottom: 10px; }
            .btn-action:hover { background: linear-gradient(135deg, #1a1529, #120f1f); color: #fff; box-shadow: 0 0 20px rgba(80, 250, 123, 0.2); }

            .contrato-container { display: none; background: rgba(0, 0, 0, 0.85); border: 1px dashed var(--cyan-neon); border-radius: 10px; padding: 20px; margin-top: 20px; }
            .contrato-header { font-size: 0.75em; color: var(--cyan-neon); font-weight: bold; border-bottom: 1px solid rgba(139, 233, 253, 0.2); padding-bottom: 8px; margin-bottom: 15px; display: flex; justify-content: space-between; }
            .contrato-body { font-size: 0.9em; color: #ffffff; line-height: 1.6; margin-bottom: 20px; background: rgba(255,255,255,0.02); padding: 15px; border-radius: 6px; border-left: 3px solid var(--magenta-neon); }
            
            .btn-firma-biometrica { background: linear-gradient(135deg, #1a0f1a, #0d050d); border: 1px solid var(--magenta-neon); color: var(--magenta-neon); padding: 14px; width: 100%; border-radius: 6px; font-family: inherit; font-weight: bold; letter-spacing: 2px; text-transform: uppercase; cursor: pointer; position: relative; overflow: hidden; }
            .btn-firma-biometrica .scan-line { position: absolute; top: 0; left: 0; width: 100%; height: 3px; background: var(--green-neon); box-shadow: 0 0 10px var(--green-neon); display: none; animation: scanMove 1.5s infinite linear; }
            @keyframes scanMove { 0% { top: 0%; } 50% { top: 100%; } 100% { top: 0%; } }

            .display-box { background: rgba(0, 0, 0, 0.65); padding: 20px; border-radius: 10px; margin-bottom: 20px; font-size: 0.95em; color: var(--yellow-neon); }
            input[type='text'] { width: 100%; background: rgba(0,0,0,0.75); border: 1px solid var(--border-dim); border-left: 3px solid var(--cyan-neon); color: #fff; padding: 15px; border-radius: 8px; box-sizing: border-box; outline: none; font-family: inherit; margin-bottom: 20px; }

            .palabra-display { display: flex; justify-content: center; gap: 8px; margin: 30px 0; flex-wrap: wrap; }
            .letra-bloque { background: rgba(0, 0, 0, 0.75); border: 1px dashed rgba(139, 233, 253, 0.25); color: var(--cyan-neon); font-size: 1.3em; font-weight: bold; width: 40px; height: 48px; display: flex; align-items: center; justify-content: center; border-radius: 8px; }
            .teclado-container { display: grid; grid-template-columns: repeat(7, 1fr); gap: 7px; }
            .tecla { background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255, 255, 255, 0.06); color: #fff; font-family: inherit; padding: 12px 0; border-radius: 6px; cursor: pointer; }
            .tecla:disabled { opacity: 0.12; }

            .heart-particle { position: fixed; color: #ff5555; font-size: 28px; animation: flyUpBrutal 1.8s forwards; pointer-events: none; z-index: 9999; }
            @keyframes flyUpBrutal { 0% { transform: translateY(0) scale(0.8); opacity: 1; } 100% { transform: translateY(-95vh) translateX(var(--random-x, 0px)) scale(1.5); opacity: 0; } }

            .footer-info { font-size: 0.65em; color: #44475a; text-align: center; margin-top: 30px; letter-spacing: 2px; text-transform: uppercase; border-top: 1px solid rgba(255,255,255,0.05); padding-top: 12px; }
            .op-badge { font-size: 0.75em; color: var(--cyan-neon); margin-bottom: 15px; text-align: center; letter-spacing: 1px; font-weight: bold; }
            
            .btn-logout { background: transparent; border: 1px solid rgba(255,121,198,0.3); color: var(--magenta-neon); font-size: 0.7em; padding: 4px 8px; border-radius: 4px; cursor: pointer; font-family: inherit; margin-left: 8px; }
        </style>
    </head>
    <body>

        <div id='splash-screen'>
            <div class='logo-tactical-wrap'>
                <div class='logo-sun-s'>S</div>
            </div>
        </div>

        <div id='identity-screen' class='access-card' style='border-top: 2px solid var(--yellow-neon);'>
            <div class='gate-warning' style="color: var(--yellow-neon);">
                👤 REGISTRO // NUEVA IDENTIDAD TÁCTICA
            </div>
            <p style='font-size:0.8em; color:#6272a4; text-transform:uppercase; margin-bottom:20px;'>Introduce tu alias de operador para este dispositivo:</p>
            <input type='text' id='input-operador' placeholder='Ej: GHOST_01, OPERADORA...' style="border-left-color: var(--yellow-neon);">
            <button class='btn-action' style="border-color: var(--yellow-neon); color: var(--yellow-neon);" onclick='guardarNuevoUsuario()'>Registrar Operador</button>
        </div>

        <div id='gatekeeper-screen' class='access-card' style='border-top: 2px solid var(--cyan-neon);'>
            <div class='gate-warning' style='color: var(--cyan-neon);'>
                🔒 SECURITY_GATE // VERIFICACIÓN REQUERIDA
            </div>
            <div id='saludo-operador' style='font-size:0.85em; color:#fff; margin-bottom:15px; text-transform:uppercase; font-weight:bold;'>OPERADOR: LOCAL_USER</div>
            <div class='trivia-box' id='box-adivinanza'>Cargando vectores...</div>
            <div class='options-grid' id='contenedor-opciones-seguridad'></div>
            <p id='gate-feedback' style='font-size:0.8em; font-weight:bold; margin-top:22px; min-height:18px; text-transform:uppercase;'></p>
            <button class='btn-logout' style='margin-top:15px; font-size:0.65em;' onclick='borrarSesion()'>Cambiar de Operador 🔄</button>
        </div>

        <div class='main-content' id='main-wrapper'>
            <div class='op-badge'>
                <span id='badge-nombre-operador'>OPERADOR: UNKNOWN</span>
                <button class='btn-logout' onclick='location.reload()'>Cerrar Terminal</button>
            </div>

            <div class='achievements-row'>
                <div class='badge' id='badge-1'>🎖️ OPERADOR EXCELSO</div>
                <div class='badge' id='badge-2'>🎖️ CONTRATISTA ÉLITE</div>
                <div class='badge' id='badge-3'>🎖️ VISIONARIO</div>
            </div>

            <div class='tabs-nav'>
                <button class='tab-btn active' onclick='cambiarVentana("win-misiones", this)'>Misiones</button>
                <button class='tab-btn' onclick='cambiarVentana("win-decrypt", this)'>Decrypt</button>
                <button class='tab-btn' onclick='cambiarVentana("win-deseos", this)'>Deseos</button>
            </div>

            <div id='win-misiones' class='window-box active'>
                <div class='window-header'>🛰️ COMPONENT // MISIONES AMBULARES V2.2</div>
                <div class='display-box' id='box-mision'>[ Sistema listo para desplegar misiones ]</div>
                <button class='btn-action' onclick='obtenerMision()'>Asignar Misión Aleatoria 🎲</button>
                <button id='btn-hacer-contrato' class='btn-action' style='display:none; border-color: var(--cyan-neon); color: var(--cyan-neon);' onclick='desplegarContrato()'>[ GENERAR CONTRATO TÁCTICO ]</button>

                <div class='contrato-container' id='bloque-contrato'>
                    <div class='contrato-header'><span id='contrato-id'>CONTRATO // #0000</span><span>STATUS: PENDING</span></div>
                    <div class='contrato-body' id='contrato-texto-mision'>Contrato vacío...</div>
                    <button id='btn-firmar' class='btn-firma-biometrica' onmousedown='iniciarFirma()' onmouseup='cancelarFirma()' onmouseleave='cancelarFirma()' ontouchstart='iniciarFirma()' ontouchend='cancelarFirma()'>
                        <div class='scan-line' id='linea-escaner'></div><span id='texto-firma'>MANTÉN PULSADO PARA FIRMA BIOMÉTRICA</span>
                    </button>
                </div>
            </div>

            <div id='win-decrypt' class='window-box'>
                <div class='window-header'>💻 COMPONENT // DECRYPT_CORE</div>
                <div style='font-size:0.75em; color:var(--magenta-neon); margin-bottom: 5px; font-weight:bold;' id='intentos-txt'>INTENTOS: 6/6</div>
                <div class='palabra-display' id='contenedor-palabra'></div>
                <div class='teclado-container' id='contenedor-teclado'></div>
                <p id='game-feedback' style='font-size:0.85em; font-weight:bold; text-align:center; min-height:18px;'></p>
                <button id='btn-restart-game' class='btn-action' style='display:none;' onclick='iniciarJuego()'>Reiniciar Encriptación 🔄</button>
            </div>

            <div id='win-deseos' class='window-box'>
                <div class='window-header'>💾 COMPONENT // CENTRAL_WISH_LOG</div>
                <form action='/guardar-deseo' method='POST' onsubmit='desbloquearLogro("3")'>
                    <input type='text' name='deseo' placeholder='Escribe un deseo aquí...' required>
                    <button type='submit' class='btn-action'>Cifrar y Guardar Deseo 💾</button>
                </form>
            </div>

            <div class='footer-info'>STATION_ID: CLOUD_NODE_01 // SECURE_SHELL</div>
        </div>

        <script>
            let operadorActivo = "";

            const bancoPreguntasSeguridad = [
                { adivinanza: "Pista: Un payaso mafioso siembra el caos con una moneda y un héroe nocturno vestido de murciélago tiene que salvar la ciudad.", correcta: "Batman: El Caballero de la Noche", falsas: ["Iron Man", "Avengers", "Spiderman"] },
                { adivinanza: "Pista: Un barco gigantesco se hunde, un dibujo en carboncillo y una tabla de madera donde claramente entraban los dos.", correcta: "Titanic", falsas: ["Poseidón", "Pearl Harbor", "Náufrago"] },
                { adivinanza: "Pista: Un ogro verde que vive en un pantano quiere soledad, pero termina rescatando a una princesa junto a un burro parlanchín.", correcta: "Shrek", falsas: ["Toy Story", "Monsters Inc", "Madagascar"] }
            ];
            let preguntaActiva = null;

            window.addEventListener('DOMContentLoaded', () => {
                setTimeout(() => {
                    document.getElementById('splash-screen').style.opacity = '0';
                    setTimeout(() => { 
                        document.getElementById('splash-screen').remove(); 
                        let guardado = localStorage.getItem('sentinel_operador_actual');
                        if (guardado) {
                            operadorActivo = guardado;
                            irAPantallaContrasena();
                        } else {
                            document.getElementById('identity-screen').style.display = 'block';
                        }
                    }, 600);
                }, 1800);
            });

            function guardarNuevoUsuario() {
                let input = document.getElementById('input-operador').value.trim().toUpperCase();
                if(!input) return;
                localStorage.setItem('sentinel_operador_actual', input);
                operadorActivo = input;
                document.getElementById('identity-screen').style.display = 'none';
                irAPantallaContrasena();
            }

            function irAPantallaContrasena() {
                document.getElementById('saludo-operador').innerText = "OPERADOR DETECTADO: " + operadorActivo;
                document.getElementById('gatekeeper-screen').style.display = 'block';
                prepararTriviaSeguridad();
                checkAchievements();
            }

            function borrarSesion() {
                localStorage.removeItem('sentinel_operador_actual');
                location.reload();
            }

            function prepararTriviaSeguridad() {
                preguntaActiva = bancoPreguntasSeguridad[Math.floor(Math.random() * bancoPreguntasSeguridad.length)];
                document.getElementById('box-adivinanza').innerText = preguntaActiva.adivinanza;
                let todasLasOpciones = [preguntaActiva.correcta, ...preguntaActiva.falsas].sort(() => Math.random() - 0.5);
                const contenedor = document.getElementById('contenedor-opciones-seguridad');
                contenedor.innerHTML = "";
                todasLasOpciones.forEach(opt => {
                    let btn = document.createElement('button');
                    btn.classList.add('btn-option-gate');
                    btn.innerText = opt;
                    btn.onclick = function() { verificarContrasenaTrivia(this.innerText); };
                    contenedor.appendChild(btn);
                });
            }

            function verificarContrasenaTrivia(opcionSeleccionada) {
                const feedback = document.getElementById('gate-feedback');
                if (opcionSeleccionada === preguntaActiva.correcta) {
                    feedback.style.color = "var(--green-neon)";
                    feedback.innerText = "✓ AUTENTICACIÓN EXITOSA // ACCESO CONCEDIDO ❤️";
                    lanzarCorazones();
                    setTimeout(() => {
                        document.getElementById('gatekeeper-screen').remove();
                        document.getElementById('badge-nombre-operador').innerText = "OPERADOR DE ENLACE: " + operadorActivo;
                        const main = document.getElementById('main-wrapper');
                        main.style.display = 'block';
                        setTimeout(() => { main.style.opacity = '1'; }, 50);
                    }, 1200);
                } else {
                    feedback.style.color = "var(--magenta-neon)";
                    feedback.innerText = "❌ CLAVE INCORRECTA // SISTEMA BLOQUEADO";
                }
            }

            function checkAchievements() {
                if(!operadorActivo) return;
                if(localStorage.getItem(operadorActivo + '_ach_1') === 'true') document.getElementById('badge-1').classList.add('unlocked');
                if(localStorage.getItem(operadorActivo + '_ach_2') === 'true') document.getElementById('badge-2').classList.add('unlocked');
                if(localStorage.getItem(operadorActivo + '_ach_3') === 'true') document.getElementById('badge-3').classList.add('unlocked');
            }

            function desbloquearLogro(num) {
                if(!operadorActivo) return;
                localStorage.setItem(operadorActivo + '_ach_' + num, 'true');
                checkAchievements();
            }

            function cambiarVentana(windowId, boton) {
                let ventanas = document.getElementsByClassName('window-box');
                for (let v of ventanas) { v.classList.remove('active'); }
                let botones = document.getElementsByClassName('tab-btn');
                for (let b of botones) { b.classList.remove('active'); }
                document.getElementById(windowId).classList.add('active');
                boton.classList.add('active');
            }

            const misiones = [
                "☕ Misión: Tarde de café y plática profunda respondiendo preguntas curiosas.",
                "🌌 Misión: Ir a un lugar tranquilo a ver las estrellas o el atardecer sin celulares.",
                "🍕 Misión: Noche de películas táctica devorando comida chatarra favorita."
            ];
            let misionActualParaContrato = "";

            function obtenerMision() {
                misionActualParaContrato = misiones[Math.floor(Math.random() * misiones.length)];
                document.getElementById('box-mision').innerText = misionActualParaContrato;
                document.getElementById('btn-hacer-contrato').style.display = "block";
                document.getElementById('bloque-contrato').style.display = "none";
                resetearBotonFirma();
            }

            function desplegarContrato() {
                document.getElementById('contrato-id').innerText = "CONTRATO_LOG // #" + Math.floor(1000 + Math.random() * 9000);
                document.getElementById('contrato-texto-mision').innerHTML = `<b>DECLARACIÓN DE COMPROMISO:</b><br>Por medio de este cifrado, ambas partes aceptan desplegar de forma obligatoria:<br><br><span style='color: var(--yellow-neon);'>${misionActualParaContrato}</span>`;
                document.getElementById('bloque-contrato').style.display = "block";
                document.getElementById('btn-hacer-contrato').style.display = "none";
            }

            let tiempoFirma;
            function iniciarFirma() {
                const btn = document.getElementById('btn-firmar');
                if(btn.disabled) return;
                document.getElementById('linea-escaner').style.display = "block";
                tiempoFirma = setTimeout(() => {
                    document.getElementById('linea-escaner').style.display = "none";
                    document.getElementById('texto-firma').innerText = "[ CONTRATO FIRMADO Y SELLADO ]";
                    btn.disabled = true;
                    lanzarCorazones();
                    desbloquearLogro("2");
                }, 1500); 
            }
            function cancelarFirma() { clearTimeout(tiempoFirma); resetearBotonFirma(); }
            function resetearBotonFirma() {
                const btn = document.getElementById('btn-firmar');
                if(btn.disabled) return;
                document.getElementById('linea-escaner').style.display = "none";
                document.getElementById('texto-firma').innerText = "MANTÉN PULSADO PARA FIRMA BIOMÉTRICA";
            }

            const palabrasSecretas = ["ABRAZO", "SONRISA", "DESTINO", "SIEMPRE", "SENTINEL"];
            let palabraElegida = ""; let letrasAdivinadas = []; let intentosRestantes = 6;

            function lanzarCorazones() {
                for(let i=0; i<15; i++) {
                    let heart = document.createElement('div'); heart.innerHTML = '❤️'; heart.classList.add('heart-particle');
                    heart.style.left = (Math.random() * 100) + 'vw'; heart.style.top = '90vh';
                    heart.style.setProperty('--random-x', (Math.random() * 200 - 100) + 'px');
                    document.body.appendChild(heart); setTimeout(() => heart.remove(), 1800);
                }
            }

            function iniciarJuego() {
                intentosRestantes = 6; letrasAdivinadas = [];
                palabraElegida = palabrasSecretas[Math.floor(Math.random() * palabrasSecretas.length)];
                document.getElementById('intentos-txt').innerText = "INTENTOS: " + intentosRestantes + "/6";
                document.getElementById('game-feedback').innerText = "";
                document.getElementById('btn-restart-game').style.display = "none";
                actualizarPantallaPalabra(); generarTeclado();
            }

            function actualizarPantallaPalabra() {
                const contenedor = document.getElementById('contenedor-palabra'); contenedor.innerHTML = "";
                for (let i = 0; i < palabraElegida.length; i++) {
                    let bloque = document.createElement('div'); bloque.classList.add('letra-bloque');
                    bloque.innerText = letrasAdivinadas.includes(palabraElegida[i]) ? palabraElegida[i] : "_";
                    contenedor.appendChild(bloque);
                }
            }

            function generarTeclado() {
                const contenedor = document.getElementById('contenedor-teclado'); contenedor.innerHTML = "";
                "ABCDEFGHIJKLMNOPQRSTUVWXYZ".split("").forEach(l => {
                    let b = document.createElement('button'); b.classList.add('tecla'); b.innerText = l;
                    b.onclick = function() {
                        this.disabled = true;
                        if(palabraElegida.includes(l)) {
                            letrasAdivinadas.push(l); actualizarPantallaPalabra();
                            if(palabraElegida.split("").every(letra => letrasAdivinadas.includes(letra))) {
                                document.getElementById('game-feedback').innerText = "✓ DATA UNLOCKED 🔓";
                                document.getElementById('btn-restart-game').style.display = "block";
                                lanzarCorazones(); desbloquearLogro("1");
                            }
                        } else {
                            intentosRestantes--; document.getElementById('intentos-txt').innerText = "INTENTOS: " + intentosRestantes + "/6";
                            if(intentosRestantes <= 0) { 
                                document.getElementById('game-feedback').innerText = "❌ SOLUCIÓN: " + palabraElegida;
                                document.getElementById('btn-restart-game').style.display = "block";
                            }
                        }
                    };
                    contenedor.appendChild(b);
                });
            }
            iniciarJuego();
        </script>
    </body>
</html>
"""

@app.route('/')
def main_page():
    return PAGINA_NUEVA

@app.route('/guardar-deseo', methods=['POST'])
def guardar_deseo():
    deseo = request.form.get('deseo')
    if deseo:
        # Se guarda de forma segura en la carpeta actual del servidor
        with open('deseos.txt', 'a', encoding='utf-8') as f:
            f.write(deseo + '\n---\n')
    return "<html><body style='background:#06040a; color:#50fa7b; font-family:monospace; text-align:center; padding:50px;'><h2>✓ ¡Deseo guardado en el servidor de la nube!</h2><br><a href='/' style='color:#8be9fd; text-decoration:none;'>Regresar</a></body></html>"

if __name__ == '__main__':
    # Render asigna el puerto automáticamente
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
