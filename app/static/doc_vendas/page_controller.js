// ================================================== \\

// ~~ Classe que controla a página.
class DocVendasPageController {

    // ~~ Atributos.
    form = document.getElementById("add_doc");
    clear_button = document.getElementById("clear_form");
    addItemButton = document.getElementById("add_item");
    itemsDiv = document.getElementById("items_div");
    itemsIndex = 0;
    parceirosDiv = document.getElementById("parceiros_div");
    addParceiroButton = document.getElementById("add_parceiro");
    parceirosIndex = 0;

    // ================================================== \\

    // ~~ Método de adicionar e remover parceiro.
    parceirosControllerInit() {

        // ~~ Event listener para ao clicar, adicionar parceiro.
        this.addParceiroButton.addEventListener("click", () => {

            // ~~ Cria linha de parceiros.
            const parceiroLinha = document.createElement("div");
            parceiroLinha.className = "md:col-span-2 flex justify-center gap-4 w-full my-3";
            parceiroLinha.id = `parceiro_linha_${this.parceirosIndex}`;

            // ~~ Cria input.
            const parceiroInput = document.createElement("input");
            parceiroInput.className = "p-2 border rounded w-full text-center";
            parceiroInput.type = "text";
            parceiroInput.name = `parceiro_${this.parceirosIndex}`;

            // ~~ Cria botão de remover.
            const parceiroRemove = document.createElement("input");
            parceiroRemove.className = "w-10 bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700";
            parceiroRemove.type = "button";
            parceiroRemove.value = "-";
            parceiroRemove.style.cursor = "pointer";

            // ~~ Adiciona event listener no botão de remover.
            parceiroRemove.addEventListener("click", () => {
                this.parceirosDiv.removeChild(parceiroLinha);
            });

            // ~~ Adiciona input e botão na linha.
            parceiroLinha.appendChild(parceiroInput);
            parceiroLinha.appendChild(parceiroRemove);

            // ~~ Adiciona linha no container principal.
            this.parceirosDiv.appendChild(parceiroLinha);

            // ~~ Itera o index dos parceiros.
            this.parceirosIndex += 1;
        });
    }

    // ================================================== \\

    // ~~ Método de adicionar e remover itens.
    itemsControllerInit() {

        // ~~ Event listener para adicionar item ao clicar em botão.
        this.addItemButton.addEventListener("click", () => {

            // ~~ Cria a linha do item.
            const itemLinha = document.createElement("div");
            itemLinha.className = "md:col-span-5 flex justify-center gap-4 w-full my-3";
            itemLinha.id = `item_linha_${this.itemsIndex}`;

            // ~~ Lista com cada campo para ser inserido na linha.
            const camposItem = [
                { label: "SKU", type: "number", name: "sku" },
                { label: "Quantidade", type: "number", name: "quantidade" },
                { label: "Valor", type: "number", name: "valor" },
                { label: "Centro", type: "text", name: "centro", datalist: "centros" },
                { label: "Depósito", type: "number", name: "deposito", datalist: "depositos" },
                { label: "Over", type: "number", name: "over" }
            ];

            // ~~ Para cada campo na lista, cria o elemento e adiciona na linha.
            camposItem.forEach((campo) => {

                // ~~ Cria div pra abrigar label e input.
                const colunaItem = document.createElement("div");

                // ~~ Cria label.
                const campoLabel = document.createElement("label");
                campoLabel.className = "block font-small text-center";
                campoLabel.innerText = campo.label;

                // ~~ Cria input.
                const campoInput = document.createElement("input");
                campoInput.className = "p-2 border rounded w-full text-center";
                campoInput.type = campo.type;
                campoInput.name = `${campo.name}_${this.itemsIndex}`;

                // ~~ Caso input tenha datalist.
                if (campo.datalist) {
                    campoInput.setAttribute("list", campo.datalist);
                }

                // ~~ Adiciona label e input na div de coluna.
                colunaItem.appendChild(campoLabel);
                colunaItem.appendChild(campoInput);

                // ~~ Adiciona coluna na linha do item.
                itemLinha.appendChild(colunaItem);
            });

            // ~~ Cria botão de remover item.
            const removeButton = document.createElement("input");
            removeButton.type = "button";
            removeButton.value = "-";
            removeButton.style.cursor = "pointer";
            removeButton.className = "w-10 mt-6 bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700";

            // ~~ Event listener no botão de remover para excluir essa linha criada ao clicar.
            removeButton.addEventListener("click", () => {
                this.itemsDiv.removeChild(itemLinha);
            });

            // ~~ Cria coluna e adiciona o botão de remover item.
            const removeButtonCol = document.createElement("div");
            removeButtonCol.appendChild(removeButton);

            // ~~ Adiciona botão de remover na linha.
            itemLinha.appendChild(removeButtonCol);

            // ~~ Adiciona linha do item no container que irá abrigar todas as linhas.
            this.itemsDiv.appendChild(itemLinha);

            // ~~ Itera o index de itens.
            this.itemsIndex += 1;
        });
    }

    // ================================================== \\

    // ~~ Método de limpar formulário.
    limpar_form() {

        // ~~ Event listener.
        this.clear_button.addEventListener("click", () => {
            this.form.reset()
        });
    }
}

// ================================================== \\

// ~~ Cria instância.
const pageController = new DocVendasPageController();

// ~~ Inicia método que controla os itens.
pageController.itemsControllerInit();

// ~~ Inicia método que controla os parceiros.
pageController.parceirosControllerInit();

// ~~ Inicia método que limpa o formulário.
pageController.limpar_form();

// ================================================== \\