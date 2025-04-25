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
    comissaoDiv = document.getElementById("comissao_div");
    addComissaoButton = document.getElementById("add_comissao");
    comissaoIndex = 0;

    // ================================================== \\

    // ~~ Método de adicionar e remover parceiro.
    parceirosControllerInit() {

        // ~~ Event listener para ao clicar, adicionar parceiro.
        this.addParceiroButton.addEventListener("click", () => {

            // ~~ Cria linha de parceiros.
            const parceiroLinha = document.createElement("div");
            parceiroLinha.className = "md:col-span-2 flex justify-center gap-4 w-full my-3";
            parceiroLinha.id = `parceiro_linha_${this.parceirosIndex}`;

            // ~~ Cria colunas para label, input e botão.
            const colunaChave = document.createElement("div");
            const colunaCodigo = document.createElement("div");
            const colunaRemover = document.createElement("div");
            colunaChave.className = "flex flex-col w-full text-center";
            colunaCodigo.className = "flex flex-col w-full text-center";
            colunaRemover.className = "flex flex-col justify-end";

            // ~~ Cria labels.
            const labelChave = document.createElement("label");
            labelChave.innerText = "Chave";
            const labelCodigo = document.createElement("label");
            labelCodigo.innerText = "Código";

            // ~~ Cria input de chave.
            const parceiroInputChave = document.createElement("input");
            parceiroInputChave.className = "p-2 border-[#0097bd] border-2 focus:border-[#8ae8ff] outline-none rounded w-full text-center";
            parceiroInputChave.type = "text";
            parceiroInputChave.name = `parceiro_chave_${this.parceirosIndex}`;

            // ~~ Cria input de código.
            const parceiroInputCodigo = document.createElement("input");
            parceiroInputCodigo.className = "p-2 border-[#0097bd] border-2 focus:border-[#8ae8ff] outline-none rounded w-full text-center";
            parceiroInputCodigo.type = "text";
            parceiroInputCodigo.name = `parceiro_codigo_${this.parceirosIndex}`;

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

            // ~~ Adiciona labels, inputs e botão nas colunas.
            colunaChave.appendChild(labelChave);
            colunaChave.appendChild(parceiroInputChave);
            colunaCodigo.appendChild(labelCodigo);
            colunaCodigo.appendChild(parceiroInputCodigo);
            colunaRemover.appendChild(parceiroRemove);

            // ~~ Adiciona input e botão na linha.
            parceiroLinha.appendChild(colunaChave);
            parceiroLinha.appendChild(colunaCodigo);
            parceiroLinha.appendChild(colunaRemover);

            // ~~ Adiciona linha no container principal.
            this.parceirosDiv.appendChild(parceiroLinha);

            // ~~ Itera o index dos parceiros.
            this.parceirosIndex += 1;
        });
    }

    // ================================================== \\

    // ~~ Método de adicionar e remover comissão.
    comissaoControllerInit() {

        // ~~ Event listener para ao clicar, adicionar parceiro.
        this.addComissaoButton.addEventListener("click", () => {

            // ~~ Cria linha de comissão.
            const comissaoLinha = document.createElement("div");
            comissaoLinha.className = "md:col-span-2 flex justify-center gap-4 w-full my-3";
            comissaoLinha.id = `comissao_linha_${this.comissaoIndex}`;

            // ~~ Cria colunas para label, input e botão.
            const colunaChave = document.createElement("div");
            const colunaCodigo = document.createElement("div");
            const colunaPorcentagem = document.createElement("div");
            const colunaRemover = document.createElement("div");
            colunaChave.className = "flex flex-col w-full text-center";
            colunaCodigo.className = "flex flex-col w-full text-center";
            colunaPorcentagem.className = "flex flex-col w-full text-center";
            colunaRemover.className = "flex flex-col justify-end";

            // ~~ Cria labels.
            const labelChave = document.createElement("label");
            labelChave.innerText = "Chave";
            const labelCodigo = document.createElement("label");
            labelCodigo.innerText = "Código";
            const labelPorcentagem = document.createElement("label");
            labelPorcentagem.innerText = "Porcentagem";

            // ~~ Cria input de chave.
            const comissaoInputChave = document.createElement("input");
            comissaoInputChave.className = "p-2 border-[#0097bd] border-2 focus:border-[#8ae8ff] outline-none rounded w-full text-center";
            comissaoInputChave.type = "text";
            comissaoInputChave.name = `comissao_chave_${this.comissaoIndex}`;

            // ~~ Cria input de código.
            const comissaoInputCodigo = document.createElement("input");
            comissaoInputCodigo.className = "p-2 border-[#0097bd] border-2 focus:border-[#8ae8ff] outline-none rounded w-full text-center";
            comissaoInputCodigo.type = "text";
            comissaoInputCodigo.name = `comissao_codigo_${this.comissaoIndex}`;

            // ~~ Cria input de porcentagem.
            const comissaoInputPorcentagem = document.createElement("input");
            comissaoInputPorcentagem.className = "p-2 border-[#0097bd] border-2 focus:border-[#8ae8ff] outline-none rounded w-full text-center";
            comissaoInputPorcentagem.type = "text";
            comissaoInputPorcentagem.name = `comissao_porcentagem_${this.comissaoIndex}`;

            // ~~ Cria botão de remover.
            const comissaoRemove = document.createElement("input");
            comissaoRemove.className = "w-10 bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700";
            comissaoRemove.type = "button";
            comissaoRemove.value = "-";
            comissaoRemove.style.cursor = "pointer";

            // ~~ Adiciona event listener no botão de remover.
            comissaoRemove.addEventListener("click", () => {
                this.comissaoDiv.removeChild(comissaoLinha);
            });

            // ~~ Adiciona labels, inputs e botão nas colunas.
            colunaChave.appendChild(labelChave);
            colunaChave.appendChild(comissaoInputChave);
            colunaCodigo.appendChild(labelCodigo);
            colunaCodigo.appendChild(comissaoInputCodigo);
            colunaPorcentagem.appendChild(labelPorcentagem);
            colunaPorcentagem.appendChild(comissaoInputPorcentagem);
            colunaRemover.appendChild(comissaoRemove);

            // ~~ Adiciona input e botão na linha.
            comissaoLinha.appendChild(colunaChave);
            comissaoLinha.appendChild(colunaCodigo);
            comissaoLinha.appendChild(colunaPorcentagem);
            comissaoLinha.appendChild(colunaRemover);

            // ~~ Adiciona linha no container principal.
            this.comissaoDiv.appendChild(comissaoLinha);

            // ~~ Itera o index dos parceiros.
            this.comissaoIndex += 1;
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
                { label: "Over", type: "number", name: "over" },
                { label: "Garantia", type: "number", name: "garantia" },
                { label: "TCL/MOU", type: "checkbox", name: "tlc_mou" }
            ];

            // ~~ Para cada campo na lista, cria o elemento e adiciona na linha.
            camposItem.forEach((campo) => {

                // ~~ Cria div pra abrigar label e input.
                const colunaItem = document.createElement("div");
                colunaItem.className = "flex flex-col justify-center w-full";

                // ~~ Cria label.
                const campoLabel = document.createElement("label");
                campoLabel.className = "block font-small text-center";
                campoLabel.innerText = campo.label;

                // ~~ Cria input.
                const campoInput = document.createElement("input");
                campoInput.className = "p-2 border-[#0097bd] border-2 focus:border-[#8ae8ff] outline-none rounded w-full text-center";
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

                // ~~ Se for o checkbox de TCL/MOU, adiciona o comportamento dinâmico.
                if (campo.label === "TCL/MOU") {

                    // ~~ Cria div com os campos extras (teclado e mouse).
                    const extrasDiv = document.createElement("div");
                    extrasDiv.className = "flex gap-2 mt-2";
                    extrasDiv.style.display = "none";

                    // ~~ Campo teclado.
                    const teclado = document.createElement("input");
                    teclado.type = "text";
                    teclado.name = `teclado_${this.itemsIndex}`;
                    teclado.placeholder = "Valor";
                    teclado.className = "p-2 border-[#0097bd] border-2 focus:border-[#8ae8ff] outline-none rounded w-full text-center";

                    // ~~ Campo mouse.
                    const mouse = document.createElement("input");
                    mouse.type = "text";
                    mouse.name = `mouse_${this.itemsIndex}`;
                    mouse.placeholder = "Valor";
                    mouse.className = "p-2 border-[#0097bd] border-2 focus:border-[#8ae8ff] outline-none rounded w-full text-center";

                    // ~~ Adiciona campos extras à div.
                    extrasDiv.appendChild(teclado);
                    extrasDiv.appendChild(mouse);

                    // ~~ Mostra ou esconde os campos com base no checkbox.
                    campoInput.addEventListener("change", () => {
                        extrasDiv.style.display = campoInput.checked ? "flex" : "none";
                        mouse.value = "";
                        teclado.value = "";
                    });

                    // ~~ Adiciona o grupo extra na coluna.
                    colunaItem.appendChild(extrasDiv);
                }

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

    // ================================================== \\

}

// ================================================== \\

// ~~ Cria instância.
const pageController = new DocVendasPageController();

// ~~ Inicia método que controla os itens.
pageController.itemsControllerInit();

// ~~ Inicia método que controla os parceiros.
pageController.parceirosControllerInit();

// ~~ Inicia método que controla os parceiros.
pageController.comissaoControllerInit();

// ~~ Inicia método que limpa o formulário.
pageController.limpar_form();

// ================================================== \\