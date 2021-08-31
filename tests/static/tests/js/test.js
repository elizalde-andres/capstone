document.addEventListener('DOMContentLoaded', function () {
    load_initial_form()
})

async function load_initial_form() {

    new_test_form = await fetch('/abm_test_layout')
    new_test_form = await new_test_form.text()
    
    await (document.querySelector("#new-test-view").innerHTML = new_test_form)

    category = document.querySelector("#test-category > select")

    load_initial_part_form(category);
    
    category.addEventListener("change",() => {
        load_initial_part_form(category);
    })

}

async function load_initial_part_form(category) {
    part_form = document.querySelector("#parts-forms");
    part_form.innerHTML = ""

    new_part_form = await fetch('/abm_testpart_layout?' + new URLSearchParams({
        category: category.options[category.selectedIndex].text,
        part_number: 1
    }))
    new_part_form = await new_part_form.text();

    await (part_form.innerHTML = new_part_form);
    load_initial_question_form(category);
}

async function load_initial_question_form(category) {
    question_forms = document.querySelector("#question-forms")
    question_forms.innerHTML = ""
    new_question_form = await fetch('/abm_question_layout?' + new URLSearchParams({
        category: category.options[category.selectedIndex].text,
        question_number: 1
    }))
    new_question_form = await new_question_form.text();

    await (question_forms.innerHTML = new_question_form);

    document.querySelector("#add-question-1").addEventListener("click", function () {
        alert("click5")
        add_question_form(question_forms, 2);
    })
}

async function add_question_form(question_forms, question_number) {
    new_question_form = await fetch('/abm_question_layout?' + new URLSearchParams({
        category: category.options[category.selectedIndex].text,
        question_number: question_number
    }))
    new_question_form = await new_question_form.text();

    await (question_forms.insertAdjacentHTML("beforeend",new_question_form));

    document.querySelector(`#add-question-${question_number}`).addEventListener("click", function () {
        alert("click6")
        add_question_form(question_forms, question_number + 1);
    })
    document.querySelector(`#delete-question-${question_number}`).addEventListener("click", function () {
        document.querySelector(`#question-form-${question_number}`).remove()
    })
}