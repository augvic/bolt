// ================================================== \\

// ~~ Importa classes.
import { Item } from "./item.js";
import { Parceiro } from "./parceiro.js";
import { Comissao } from "./comissao.js";

// ================================================== \\

// ~~ Classe que controla os itens.
class ItensController {

    // ================================================== \\

    // ~~ Atributos.
    itensDiv = document.getElementById("items_div");
    itensIndex = 0
    addItemButton = document.getElementById("add_item");

    // ================================================== \\

    // ~~ Método que adiciona itens.
    adicionarItem() {

        // ~~ Event listener no botão de adicionar.
        this.addItemButton.addEventListener("click", () => {

            // ~~ Cria nova linha de item.
            const item = new Item();

            // ~~ Define os "names" de cada input.
            item.sku.name = `sku_${this.itensIndex}`;
            item.quantidade.name = `quantidade_${this.itensIndex}`;
            item.valorUnitario.name = `valor_unitario_${this.itensIndex}`;
            item.valorTotal.name = `valor_total_${this.itensIndex}`;
            item.centro.name = `centro_${this.itensIndex}`;
            item.deposito.name = `deposito_${this.itensIndex}`;
            item.over.name = `over_${this.itensIndex}`;
            item.garantia.name = `garantia_${this.itensIndex}`;
            item.teclado.name = `teclado_${this.itensIndex}`;
            item.mouse.name = `mouse_${this.itensIndex}`;

            // ~~ Adiciona a linha no container de itens.
            this.itensDiv.appendChild(item.itemLinha);

            // ~~ Adiciona event listener no botão de remover.
            item.removeButton.addEventListener("click", () => {

                // ~~ Remove a linha do container de itens.
                this.itensDiv.removeChild(item.itemLinha);
            });

            // ~~ Itera o index dos itens adicionados.
            this.itensIndex += 1;
        });
    }

    // ================================================== \\

}

// ================================================== \\

// ~~ Classe que controla os parceiros.
class ParceirosController {

    // ================================================== \\

    // ~~ Atributos.
    parceirosDiv = document.getElementById("parceiros_div");
    parceirosIndex = 0
    addParceiroButton = document.getElementById("add_parceiro");

    // ================================================== \\

    // ~~ Método que adiciona itens.
    adicionarParceiro() {

        // ~~ Event listener no botão de adicionar.
        this.addParceiroButton.addEventListener("click", () => {

            // ~~ Cria nova linha de parceiro.
            const parceiro = new Parceiro();

            // ~~ Define os "names" de cada input.
            parceiro.parceiroInputChave.name = `parceiro_chave_${this.parceirosIndex}`;
            parceiro.parceiroInputCodigo.name = `parceiro_codigo_${this.parceirosIndex}`;

            // ~~ Adiciona a linha no container de itens.
            this.parceirosDiv.appendChild(parceiro.parceiroLinha);

            // ~~ Adiciona event listener no botão de remover.
            parceiro.parceiroRemove.addEventListener("click", () => {

                // ~~ Remove a linha do container de itens.
                this.parceirosDiv.removeChild(parceiro.parceiroLinha);
            });

            // ~~ Itera o index dos itens adicionados.
            this.parceirosIndex += 1;
        });
    }

    // ================================================== \\

}

// ================================================== \\

// ~~ Classe que controla as comissões.
class ComissoesController {

    // ================================================== \\

    // ~~ Atributos.
    comissaoDiv = document.getElementById("comissao_div");
    comissaoIndex = 0
    addComissaoButton = document.getElementById("add_comissao");

    // ================================================== \\

    // ~~ Método que adiciona itens.
    adicionarComissao() {

        // ~~ Event listener no botão de adicionar.
        this.addComissaoButton.addEventListener("click", () => {

            // ~~ Cria nova linha de comissão.
            const comissao = new Comissao();

            // ~~ Define os "names" de cada input.
            comissao.comissaoInputChave.name = `comissao_chave_${this.comissaoIndex}`;
            comissao.comissaoInputCodigo.name = `comissao_codigo_${this.comissaoIndex}`;
            comissao.comissaoInputPorcentagem.name = `comissao_porcentagem_${this.comissaoIndex}`;

            // ~~ Adiciona a linha no container de itens.
            this.comissaoDiv.appendChild(comissao.comissaoLinha);

            // ~~ Adiciona event listener no botão de remover.
            comissao.comissaoRemove.addEventListener("click", () => {

                // ~~ Remove a linha do container de itens.
                this.comissaoDiv.removeChild(comissao.comissaoLinha);
            });

            // ~~ Itera o index dos itens adicionados.
            this.comissaoIndex += 1;
        });
    }

    // ================================================== \\

}

// ================================================== \\

// ~~ Classe que controla o formulário.
class FormController {

    // ================================================== \\

    // ~~ Atributos.
    form = document.getElementById("add_doc");
    clearButton = document.getElementById("clear_form");

    // ================================================== \\

    // ~~ Método de limpar formulário.
    limpar_form() {

        // ~~ Event listener ao clicar no botão.
        this.clearButton.addEventListener("click", () => {

            // ~~ Reseta o formulário.
            this.form.reset()

            // ~~ Coleta as divs de teclado e mouse.
            const divsExtras = document.querySelectorAll("[id^='id_tcl_mou_']");

            // ~~ Para cada div de teclado e mouse, muda o display para none.
            divsExtras.forEach(div => {
                div.style.display = "none";
            });
        });
    }

    // ================================================== \\

}

// ================================================== \\

// ~~ Classe que gerencia o CRUD dos documentos.
class DocsController {

    // ================================================== \\

    // ~~ Atributos.
    visualizarFilaButton = document.getElementById("visualizar_fila");
    fecharFilaButton = document.getElementById("fechar_fila");
    modalFila = document.getElementById("modal_fila");
    addFilaButton = document.getElementById("add_fila");
    modalContainer = document.getElementById("modal_fila_container");

    // ================================================== \\

    // ~~ Função que fecha o modal de fila.
    fecharFila() {

        // ~~ Event listener.
        this.fecharFilaButton.addEventListener("click", () => {

            // ~~ Adiciona class hidden no modal.
            this.modalFila.classList.add('hidden');

            // ~~ Remove class flex no modal.
            this.modalFila.classList.remove('flex');

            // ~~ Adiciona o overflow no body novamente.
            document.getElementById('body').classList.remove('overflow-hidden');
        });
    }

    // ================================================== \\

    // ~~ Função que abre o modal de fila.
    visualizarFila() {

        // ~~ Event listener no botão.
        this.visualizarFilaButton.addEventListener("click", () => {

            // ~~ Remove classe hidden.
            this.modalFila.classList.remove("hidden");

            // ~~ Adiciona classe flex.
            this.modalFila.classList.add("flex");

            // ~~ Remove scroll do body da página no fundo.
            const scrollBody = document.getElementById("body");
            scrollBody.classList.add("overflow-hidden");

            // ~~ Carrega os registros.
            // this.carregarFila();
        });
    }

    // ================================================== \\

    // ~~ Função que carrega os registros.
    async carregarFila() {

        // ~~ Faz fetch para coletar dados do banco.
        const resposta = await fetch("./coletar-registros");
        const data = await resposta.json();

        // ~~ Limpa conteúdo que estava no container.
        this.modalContainer.innerHTML = "";

        // ~~ Cria linha.
        const linha = document.createElement("div");
        linha.className = "flex w-full gap-4";

        // ~~ Cria colunas que ficarão na linha.

    }

    // ================================================== \\

    // ~~ Função que faz fetch no endpoint de adicionar documento na fila.
    adicionarNaFila() {

        // ~~ Event listener no botão.
        this.addFilaButton.addEventListener("click", () => {

            // ~~ Localiza form.
            const formElement = document.querySelector("#add_doc");

            // ~~ Verifica se os campos estão preenchidos.
            if (!formElement.checkValidity()) {
                formElement.reportValidity();
                return;
            }

            // ~~ Cria instância com dados do form.
            const formData = new FormData(formElement);

            // ~~ Faz fetch para o endpoint.
            fetch("./adicionar-na-fila", {
                method: "POST",
                body: formData
            })

            // ~~ Pega resposta e converte pra JSON.
            .then(response => response.json())

            // ~~ Pega resposta.
            .then(data => {

                // ~~ Se houve sucesso.
                if (data.sucesso) {
                    this.mostrarPopup("Adicionado na fila.", true);

                // ~~ Se não houve sucesso.
                } else {
                    this.mostrarPopup("Erro ao adicionar na fila.", false);
                }
            });
        });
    }

    // ================================================== \\

    // ~~ Função que exibe um popup no retorno da resposta do backend.
    mostrarPopup(mensagem, sucesso) {
        const popup = document.createElement("div");
        popup.className = `
            fixed top-4 left-1/2 transform -translate-x-1/2 
            px-6 py-3 rounded-lg shadow-lg text-white z-50
            transition-opacity duration-300
            ${sucesso ? 'bg-green-600' : 'bg-red-600'}
        `;
        popup.innerText = mensagem;
        document.body.appendChild(popup);
        setTimeout(() => {
            popup.style.opacity = '0';
            setTimeout(() => popup.remove(), 300);
        }, 3000);
    }

    // ================================================== \\

}

// ================================================== \\

// ~~ Cria instâncias.
const itensController = new ItensController();
const parceirosController = new ParceirosController();
const comissoesController = new ComissoesController();
const formController = new FormController();
const docsController = new DocsController();

// ~~ Executa métodos.
itensController.adicionarItem();
parceirosController.adicionarParceiro();
comissoesController.adicionarComissao();
formController.limpar_form();
docsController.visualizarFila();
docsController.adicionarNaFila();
docsController.fecharFila();

// ================================================== \\