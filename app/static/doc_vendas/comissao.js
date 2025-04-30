// ================================================== \\

/**
 * Resumo:
 *  - Classe usada para criar uma comissão na página dinamicamente.
 */

// ~~ Classe de comissões.
export class Comissao {

    // ================================================== \\

    // ~~ Construtor.
    constructor() {

        // ~~ Cria linha de comissão.
        this.comissaoLinha = document.createElement("div");
        this.comissaoLinha.className = "md:col-span-2 flex justify-center gap-4 w-full mt-4";

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
        this.comissaoInputChave = document.createElement("input");
        this.comissaoInputChave.className = "p-2 border-[#0097bd] border-2 focus:border-[#8ae8ff] outline-none rounded w-full text-center";
        this.comissaoInputChave.type = "text";

        // ~~ Cria input de código.
        this.comissaoInputCodigo = document.createElement("input");
        this.comissaoInputCodigo.className = "p-2 border-[#0097bd] border-2 focus:border-[#8ae8ff] outline-none rounded w-full text-center";
        this.comissaoInputCodigo.type = "text";

        // ~~ Cria input de porcentagem.
        this.comissaoInputPorcentagem = document.createElement("input");
        this.comissaoInputPorcentagem.className = "p-2 border-[#0097bd] border-2 focus:border-[#8ae8ff] outline-none rounded w-full text-center";
        this.comissaoInputPorcentagem.type = "text";
        this.comissaoInputPorcentagem.name = `comissao_porcentagem_${this.comissaoIndex}`;

        // ~~ Cria botão de remover.
        this.comissaoRemove = document.createElement("input");
        this.comissaoRemove.className = "w-10 bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700";
        this.comissaoRemove.type = "button";
        this.comissaoRemove.value = "-";
        this.comissaoRemove.style.cursor = "pointer";

        // ~~ Adiciona labels, inputs e botão nas colunas.
        colunaChave.appendChild(labelChave);
        colunaChave.appendChild(this.comissaoInputChave);
        colunaCodigo.appendChild(labelCodigo);
        colunaCodigo.appendChild(this.comissaoInputCodigo);
        colunaPorcentagem.appendChild(labelPorcentagem);
        colunaPorcentagem.appendChild(this.comissaoInputPorcentagem);
        colunaRemover.appendChild(this.comissaoRemove);

        // ~~ Adiciona input e botão na linha.
        this.comissaoLinha.appendChild(colunaChave);
        this.comissaoLinha.appendChild(colunaCodigo);
        this.comissaoLinha.appendChild(colunaPorcentagem);
        this.comissaoLinha.appendChild(colunaRemover);

        // ~~ Retorna elemento.
        return this;
    }

    // ================================================== \\

}

// ================================================== \\