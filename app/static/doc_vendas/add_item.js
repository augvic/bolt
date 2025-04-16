const add_button = document.getElementById("add_item");

add_button.addEventListener("click", () => {
    const container = document.getElementById("items_div");

    const index = container.children.length; // Cada filho é uma linha de item
    const prefix = `item_${index}`;

    // Cria a linha do item
    const itemRow = document.createElement("div");
    itemRow.className = "md:col-span-5 flex justify-center gap-4 w-full";

    const fields = [
        { label: "SKU", type: "number", name: "sku" },
        { label: "Quantidade", type: "number", name: "quantidade" },
        { label: "Valor", type: "number", name: "valor" },
        { label: "Centro", type: "text", name: "centro", datalist: "centros" },
        { label: "Depósito", type: "number", name: "deposito", datalist: "depositos" },
        { label: "Over", type: "number", name: "over" }
    ];

    fields.forEach((f) => {
        const fieldDiv = document.createElement("div");

        const label = document.createElement("label");
        label.className = "block font-small text-center";
        label.innerText = f.label;

        const input = document.createElement("input");
        input.type = f.type;
        input.name = `${prefix}_${f.name}`;
        input.className = "p-2 border rounded w-full text-center";

        if (f.datalist) {
            input.setAttribute("list", f.datalist);
        }

        fieldDiv.appendChild(label);
        fieldDiv.appendChild(input);
        itemRow.appendChild(fieldDiv);
    });

    // Botão de deletar
    const deleteDiv = document.createElement("div");

    const deleteBtn = document.createElement("input");
    deleteBtn.type = "button";
    deleteBtn.value = "-";
    deleteBtn.style.cursor = "pointer";
    deleteBtn.className = "w-10 mt-6 bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700";

    deleteBtn.addEventListener("click", () => {
        container.removeChild(itemRow);
    });

    deleteDiv.appendChild(deleteBtn);
    itemRow.appendChild(deleteDiv);

    container.appendChild(itemRow);
});