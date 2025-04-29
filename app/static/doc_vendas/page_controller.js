// ================================================== \\

// ~~ Importa classe de item.
import { Item } from "./item.js";

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
            item.centro.name = `centro_${this.itensIndex}`;
            item.deposito.name = `deposito_${this.itensIndex}`;
            item.over.name = `over_${this.itensIndex}`;
            item.garantia.name = `garantia_${this.itensIndex}`;
            item.valorTotal.name = `valot_total_${this.itensIndex}`;
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

// ~~ Cria instâncias.
const itensController = new ItensController();
const formController = new FormController();

// ~~ Executa métodos.
itensController.adicionarItem();
formController.limpar_form();

// ================================================== \\