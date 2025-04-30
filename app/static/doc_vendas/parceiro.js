// ================================================== \\

/**
 * Resumo:
 *  - Classe usada para criar um parceiro na página dinamicamente.
 */

// ~~ Classe de itens.
export class Parceiro {

    // ================================================== \\

    // ~~ Construtor.
    constructor() {

        // ~~ Cria linha de parceiros.
        this.parceiroLinha = document.createElement("div");
        this.parceiroLinha.className = "md:col-span-2 flex justify-center gap-4 w-full mt-4";
        this.parceiroLinha.id = `parceiro_linha_${this.parceirosIndex}`;

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
        labelChave.className = "block font-small text-center relative group"
        const labelCodigo = document.createElement("label");
        labelCodigo.innerText = "Código";
        labelCodigo.className = "block font-small text-center relative group"

        // ~~ Cria strong e faz append nos labels.
        const strong1 = document.createElement("strong");
        const strong2 = document.createElement("strong");
        strong1.innerText = " *";
        strong1.className = "text-red-600"
        strong2.innerText = " *";
        strong2.className = "text-red-600"
        labelChave.appendChild(strong1);
        labelCodigo.appendChild(strong2);

        // ~~ Cria spans de obrigatório e faz append nos labels.
        const span1 = document.createElement("span");
        const span2 = document.createElement("span");
        span1.className = "absolute hidden group-hover:block bg-gray-700 text-white text-xs rounded py-1 px-2 bottom-full left-1/2 transform -translate-x-1/2 whitespace-nowrap";
        span2.className = "absolute hidden group-hover:block bg-gray-700 text-white text-xs rounded py-1 px-2 bottom-full left-1/2 transform -translate-x-1/2 whitespace-nowrap";
        span1.innerText = "Obrigatório";
        span2.innerText = "Obrigatório";
        labelChave.appendChild(span1);
        labelCodigo.appendChild(span2);

        // ~~ Cria input de chave.
        this.parceiroInputChave = document.createElement("input");
        this.parceiroInputChave.className = "p-2 border-[#0097bd] border-2 focus:border-[#8ae8ff] outline-none rounded w-full text-center";
        this.parceiroInputChave.type = "text";
        this.parceiroInputChave.required = true;

        // ~~ Cria input de código.
        this.parceiroInputCodigo = document.createElement("input");
        this.parceiroInputCodigo.className = "p-2 border-[#0097bd] border-2 focus:border-[#8ae8ff] outline-none rounded w-full text-center";
        this.parceiroInputCodigo.type = "text";
        this.parceiroInputCodigo.required = true;

        // ~~ Cria botão de remover.
        this.parceiroRemove = document.createElement("input");
        this.parceiroRemove.className = "w-10 bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700";
        this.parceiroRemove.type = "button";
        this.parceiroRemove.value = "-";
        this.parceiroRemove.style.cursor = "pointer";

        // ~~ Adiciona labels, inputs e botão nas colunas.
        colunaChave.appendChild(labelChave);
        colunaChave.appendChild(this.parceiroInputChave);
        colunaCodigo.appendChild(labelCodigo);
        colunaCodigo.appendChild(this.parceiroInputCodigo);
        colunaRemover.appendChild(this.parceiroRemove);

        // ~~ Adiciona input e botão na linha.
        this.parceiroLinha.appendChild(colunaChave);
        this.parceiroLinha.appendChild(colunaCodigo);
        this.parceiroLinha.appendChild(colunaRemover);

        // ~~ Retorna elemento.
        return this;
    }

    // ================================================== \\

}

// ================================================== \\