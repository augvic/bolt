// ================================================== \\

/**
 * Resumo:
 *  - Classe usada para criar um item na página dinamicamente.
 */

// ~~ Classe de itens.
export class Item {

    // ================================================== \\

    // ~~ Construtor.
    constructor() {

        // ~~ IMask - Inclui automaticamente separadores de milhar e decimais.
        this.maskOptions = {
            mask: Number,
            scale: 2,
            signed: false,
            thousandsSeparator: '.',
            padFractionalZeros: true,
            normalizeZeros: true,
            radix: ',',
            mapToRadix: ['.']
        };

        // ~~ Cria a linha do item.
        this.itemLinha = document.createElement("div");
        this.itemLinha.className = "md:col-span-5 flex justify-center gap-4 w-full mt-4";

        // ~~ Lista com cada campo para ser inserido na linha.
        const camposItem = [
            { label: "SKU", type: "text", name: "sku" },
            { label: "Quantidade", type: "text", name: "quantidade" },
            { label: "Valor Unitário", type: "text", name: "valor_unitario" },
            { label: "Centro", type: "text", name: "centro", datalist: "centros" },
            { label: "Depósito", type: "text", name: "deposito", datalist: "depositos" },
            { label: "Over", type: "text", name: "over" },
            { label: "Garantia", type: "text", name: "garantia", datalist: "garantias" },
            { label: "Valor Total", type: "text", name: "valor_total" },
            { label: "TCL/MOU", type: "checkbox", name: "tcl_mou" }
        ];

        // ~~ Lista com campos não obrigatórios de preenchimento.
        const camposNaoObrigatorios = [
            "Depósito",
            "Over",
            "Garantia",
            "TCL/MOU",
            "Valor Total"
        ]

        // ~~ Para cada campo na lista, cria o elemento e adiciona na linha.
        camposItem.forEach((campo) => {

            // ~~ Cria div pra abrigar label e input.
            const colunaItem = document.createElement("div");
            colunaItem.className = "flex flex-col justify-center w-full";

            // ~~ Cria label.
            const campoLabel = document.createElement("label");
            campoLabel.className = "block font-small text-center relative group";
            campoLabel.innerText = campo.label;

            // ~~ Cria input.
            const campoInput = document.createElement("input");
            campoInput.className = "p-2 border-[#0097bd] border-2 focus:border-[#8ae8ff] outline-none rounded w-full text-center";
            campoInput.type = campo.type;
            campoInput.name = campo.name;

            // ~~ Caso input tenha datalist, atribui o datalist à ele.
            if (campo.datalist) {
                campoInput.setAttribute("list", campo.datalist);
            }

            // ~~ Verifica se campo é obrigatório para criar o indicador de obrigatoriedade.
            if (!camposNaoObrigatorios.includes(campo.label)) {

                // ~~ Cria strong.
                const strong = document.createElement("strong");
                strong.innerText = " *";
                strong.className = "text-red-600";
                campoLabel.appendChild(strong);

                // ~~ Cria o span.
                const span = document.createElement("span");
                span.className = "absolute hidden group-hover:block bg-gray-700 text-white text-xs rounded py-1 px-2 bottom-full left-1/2 transform -translate-x-1/2 whitespace-nowrap";
                span.innerText = "Obrigatório";
                campoLabel.appendChild(span);

                // ~~ Define input como required.
                campoInput.required = true;
            }

            // ~~ Adiciona label e input na div de coluna.
            colunaItem.appendChild(campoLabel);
            colunaItem.appendChild(campoInput);

            // ~~ Adiciona coluna na linha do item.
            this.itemLinha.appendChild(colunaItem);

            // ~~ Se input for "SKU".
            if (campoInput.name == "sku") {
                this.sku = campoInput;
            }

            // ~~ Se input for "quantidade".
            if (campoInput.name == "quantidade") {

                // ~~ Armazena input como atributo.
                this.quantidade = campoInput;

                // ~~ Event listener de input.
                this.quantidade.addEventListener("input", () => {

                    // ~~ Recalcula valor total.
                    this.recalcularValorTotal();

                    // ~~ Verifica se o campo está em branco.
                    if (this.quantidade.value == "") {

                        // ~~ Reseta o campo de valor total.
                        this.valorTotal.value = "";
                    }
                });
            }

            // ~~ Se input for "valor_unitario".
            if (campoInput.name == "valor_unitario") {

                // ~~ Salva o input como atributo.
                this.valorUnitario = campoInput;

                // ~~ Define valor inicial do atributo.
                this.valorUnitario.setAttribute("ultimo_valor", 0);

                // ~~ Cria a mask do input de valor unitário.
                this.valorUnitarioMask = IMask(this.valorUnitario, this.maskOptions);

                // ~~ Adiciona event listener.
                this.valorUnitario.addEventListener("input", () => {

                    // ~~ Coleta o valor digitado e converte para float.
                    const valorDigitado = this.valorUnitarioMask.unmaskedValue;

                    // ~~ Coleta o valor digitado e armazena como atributo no mesmo elemento.
                    this.valorUnitario.setAttribute("ultimo_valor", valorDigitado || "0");

                    // ~~ Recalcula valor total.
                    this.recalcularValorTotal();

                    // ~~ Verifica se inputs de teclado, mouse e garantia estão preenchidos.
                    if (this.garantia.value != "" || this.teclado.value != "" || this.mouse.value != "" ) {

                        // ~~ Reseta inputs.
                        this.garantia.value = "";
                        this.garantiaValor.value = "";
                        this.teclado.value = "";
                        this.mouse.value = "";
                    }

                    // ~~ Se o input estiver em branco.
                    if (this.valorUnitario.value == "") {

                        // ~~ Reseta o campo de valor total.
                        this.valorTotal.value = "";
                    }
                });
            }

            // ~~ Se input for "centro".
            if (campoInput.name == "centro") {

                // ~~ Armazena input como atributo.
                this.centro = campoInput;
            }

            // ~~ Se input for "depósito".
            if (campoInput.name == "deposito") {

                // ~~ Armazena input como atributo.
                this.deposito = campoInput;
            }
        
            // ~~ Se input for "over".
            if (campoInput.name == "over") {

                // ~~ Armazena input como atributo.
                this.over = campoInput;

                // ~~ Cria a mask do input de valor over.
                this.overMask = IMask(this.over, this.maskOptions);
            }

            // ~~ Se input for "garantia".
            if (campoInput.name == "garantia") {

                // ~~ Armazena garantia como atributo.
                this.garantia = campoInput;

                // ~~ Cria input escondido para armazenar valor da garantia.
                this.garantiaValor = document.createElement("input");
                this.garantiaValor.style.display = "none";
                this.garantiaValor.value = 0;
                colunaItem.appendChild(this.garantiaValor);

                // ~~ Event listener de click.
                this.garantia.addEventListener("click", () => {
                    
                    // ~~ Verifica se campo de valor unitário está preenchido.
                    if (this.valorUnitario.value == "") {

                        // ~~ Exibe alerta.
                        alert("Insira primeiro o valor unitário.");
                    }
                });

                // ~~ Event listener de input.
                this.garantia.addEventListener("input", () => {

                    // ~~ Verifica primeiro se o campo está em branco.
                    if (this.garantia.value == "") {

                        // ~~ Reseta valor da garantia para "0".
                        this.garantiaValor.value = 0;
                    }

                    // ~~ Verifica se campo de valor unitário está preenchido.
                    if (this.valorUnitario.value == "") {

                        // ~~ Exibe alerta.
                        alert("Insira primeiro o valor unitário.");

                        // ~~ Limpa campo.
                        this.garantia.value = "";
                    }

                    // ~~ Pega a descrição da garantia que está no input.
                    const descricaoGarantia = this.garantia.value;
                    
                    // ~~ Pega o datalist das garantias.
                    const datalistGarantias = document.getElementById("garantias");

                    // ~~ Coleta as opções do datalist.
                    const opcoes = datalistGarantias.querySelectorAll("option");
                    
                    // ~~ Faz loop nas opções.
                    for (let opcao of opcoes) {

                        // ~~ Se a descrição da opção bater com a opção selecionada.
                        if (opcao.value == descricaoGarantia) {

                            // ~~ Armazena valor no input de valor.
                            this.garantiaValor.value = opcao.getAttribute("valor");

                            // ~~ Atualiza o input de garantia com o código.
                            this.garantia.value = opcao.getAttribute("codigo");
                        }
                    }
                    
                    // ~~ Recalcula valor unitário.
                    this.recalcularValorUnitario();

                    // ~~ Recalcula valor total.
                    this.recalcularValorTotal();
                });
            }

            // ~~ Se input for "valor_total".
            if (campoInput.name == "valor_total") {

                // ~~ Armazena input como atributo.
                this.valorTotal = campoInput;

                // ~~ Event listener de input.
                this.valorTotal.addEventListener("input", () => {

                    // ~~ Verifica se o campo de quantidade e valor unitário estão preenchidos.
                    if (this.quantidade.value != "" && this.valorUnitario.value != "") {

                        // ~~ Multiplica o valor unitário pela quantidade.
                        const valorTotal = this.valorUnitario.value * this.quantidade.value;

                        // ~~ Converte para formato brasileiro.
                        const valorFormatado = valorTotal.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
                        
                        // ~~ Insere o valor total no seu campo.
                        this.valorTotal.value = valorFormatado;

                    // ~~ Se não estiverem.
                    } else {
                        
                        // ~~ Limpa o que o usuário inputar no campo.
                        this.valorTotal.value = "";
                    }
                });
            }

            // ~~ Se input for "tcl_mou".
            if (campoInput.name == "tcl_mou") {

                // ~~ Cria div com os campos extras (teclado e mouse).
                const extrasDiv = document.createElement("div");
                extrasDiv.className = "relative group flex gap-2 mt-2";
                extrasDiv.style.display = "none";
                extrasDiv.id = `id_tcl_mou_${this.itemsIndex}`;

                // ~~ Campo teclado.
                this.teclado = document.createElement("input");
                this.teclado.type = "text";
                this.teclado.name = `teclado_${this.itemsIndex}`;
                this.teclado.placeholder = "R$";
                this.teclado.className = "p-2 border-[#0097bd] border-2 focus:border-[#8ae8ff] outline-none rounded w-full text-center";

                // ~~ Campo mouse.
                this.mouse = document.createElement("input");
                this.mouse.type = "text";
                this.mouse.name = `mouse_${this.itemsIndex}`;
                this.mouse.placeholder = "R$";
                this.mouse.className = "p-2 border-[#0097bd] border-2 focus:border-[#8ae8ff] outline-none rounded w-full text-center";

                // ~~ Adiciona campos extras à div.
                extrasDiv.appendChild(this.teclado);
                extrasDiv.appendChild(this.mouse);

                // ~~ Cria indicador de obrigatoriedade.
                const strong = document.createElement("strong");
                strong.innerText = " *";
                strong.className = "text-red-600";
                extrasDiv.appendChild(strong);
                const span = document.createElement("span");
                span.className = "absolute hidden group-hover:block bg-gray-700 text-white text-xs rounded py-1 px-2 top-full left-1/2 transform -translate-x-1/2 whitespace-nowrap mt-2";
                span.innerText = "Obrigatório";
                extrasDiv.appendChild(span);

                // ~~ Cria mask do teclado e mouse.
                this.tecladoMask = IMask(this.teclado, this.maskOptions);
                this.mouseMask = IMask(this.mouse, this.maskOptions);

                // ~~ Event listener de click no mouse.
                this.mouse.addEventListener("click", () => {

                    // ~~ Verifica se o input de valor unitário está em branco.
                    if (this.valorUnitario.value == "") {
                        
                        // ~~ Exibe alerta.
                        alert("Insira primeiro o valor unitário.")

                        // ~~ Limpa campo.
                        this.mouse.value = "";
                    }
                });

                // ~~ Event listener de click no teclado.
                this.teclado.addEventListener("click", () => {

                    // ~~ Verifica se o input de valor unitário está em branco.
                    if (this.valorUnitario.value == "") {
                        
                        // ~~ Exibe alerta.
                        alert("Insira primeiro o valor unitário.")

                        // ~~ Limpa o campo.
                        this.teclado.value = "";
                    }
                });

                // ~~ Event listener de input no teclado.
                this.teclado.addEventListener("input", () => {

                    // ~~ Verifica se o input de valor unitário está em branco.
                    if (this.valorUnitario.value == "") {
                        
                        // ~~ Exibe alerta.
                        alert("Insira primeiro o valor unitário.")

                        // ~~ Limpa o campo.
                        this.teclado.value = "";
                    }

                    // ~~ Recalcula valor unitário.
                    this.recalcularValorUnitario();

                    // ~~ Recalcula valor total.
                    this.recalcularValorTotal();
                });

                // ~~ Event listener de input no mouse.
                this.mouse.addEventListener("input", () => {

                    // ~~ Verifica se o input de valor unitário está em branco.
                    if (this.valorUnitario.value == "") {
                        
                        // ~~ Exibe alerta.
                        alert("Insira primeiro o valor unitário.")

                        // ~~ Limpa o campo.
                        this.mouse.value = "";
                    }

                    // ~~ Recalcula valor unitário.
                    this.recalcularValorUnitario();

                    // ~~ Recalcula valor total.
                    this.recalcularValorTotal();
                });

                // ~~ Event listener no checkbox.
                campoInput.addEventListener("change", () => {

                    // ~~ Exibe e esconde os inputs de valores.
                    extrasDiv.style.display = campoInput.checked ? "flex" : "none";

                    // ~~ Limpa os inputs.
                    this.mouseMask.value = "";
                    this.tecladoMask.value = "";

                    // ~~ Define o required dos inputs.
                    this.teclado.required = campoInput.checked ? true : false;
                    this.mouse.required = campoInput.checked ? true : false;

                    // ~~ Coleta o último valor digitado.
                    const ultimoValor = this.valorUnitario.getAttribute("ultimo_valor");

                    // ~~ Verifica se havia valor.
                    if (ultimoValor == 0) {

                        // ~~ Se não havia, define valor do input para "", para não ficar com "0" ao desmarcar o checkbox.
                        this.valorUnitario.value = "";
                    } else {

                        // ~~ Se havia valor, restaura o valor que está armazenado no atributo.
                        this.recalcularValorUnitario();

                        // ~~ Recalcula valor total.
                        this.recalcularValorTotal();
                    }
                });

                // ~~ Adiciona o grupo extra na coluna.
                colunaItem.appendChild(extrasDiv);
            }
        });

        // ~~ Cria botão de remover item.
        this.removeButton = document.createElement("input");
        this.removeButton.type = "button";
        this.removeButton.value = "-";
        this.removeButton.style.cursor = "pointer";
        this.removeButton.className = "w-10 mt-6 bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700";

        // ~~ Cria coluna e adiciona o botão de remover item.
        const removeButtonCol = document.createElement("div");
        removeButtonCol.appendChild(this.removeButton);

        // ~~ Adiciona botão de remover na linha.
        this.itemLinha.appendChild(removeButtonCol);

        // ~~ Retorna a instância.
        return this;
    }

    // ================================================== \\

    // ~~ Função para recalcular o valor total.
    recalcularValorTotal() {

        // ~~ Verifica se o campo de quantidade está preenchido.
        if (this.quantidade.value != "" && this.valorUnitario.value != "") {

            // ~~ Coleta o valor digitado e converte para float.
            const valorDigitado = this.valorUnitarioMask.unmaskedValue;

            // ~~ Multiplica o valor unitário pela quantidade.
            const valorTotal = valorDigitado * this.quantidade.value;

            // ~~ Converte para formato brasileiro.
            const valorFormatado = valorTotal.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
            
            // ~~ Insere o valor total no seu campo.
            this.valorTotal.value = valorFormatado;
        }  
    }

    // ================================================== \\

    // ~~ Função para recalcular o valor unitário.
    recalcularValorUnitario() {

        // ~~ Pega valor unitário do item.
        const valor = this.valorUnitario.getAttribute("ultimo_valor");
    
        // ~~ Verifica se há algum valor no campo.
        if (valor && valor != 0) {
    
            // ~~ Pega o valor da garantia.
            const valorGarantia = parseFloat(this.garantiaValor.value) || 0;
    
            // ~~ Pega o valor do mouse.
            const valorMouse = this.mouseMask.unmaskedValue || 0;
    
            // ~~ Pega o valor do teclado.
            const valorTeclado = this.tecladoMask.unmaskedValue || 0;
    
            // ~~ Calcula novo valor.
            const novoValor = (valor - valorMouse - valorTeclado - valorGarantia);
    
            // ~~ Exibe valor atualizado no input.
            this.valorUnitarioMask.unmaskedValue = novoValor.toFixed(2);
        }
    }

    // ================================================== \\

}

// ================================================== \\