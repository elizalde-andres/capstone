let part_number = 1
let question_number = 1
let starting_part_question = 1

document.addEventListener('DOMContentLoaded', function () {
    load_form()
})

async function load_form() {

    new_test_form = await fetch('/abm_test_layout')
    new_test_form = await new_test_form.text()
    
    await (document.querySelector("#new-test-view").innerHTML = new_test_form)

    category = document.querySelector("#test-category > select")
    
    category.addEventListener("change",() => {
        document.querySelector("#parts-forms").innerHTML = ""
        if (category.options[category.selectedIndex].text != ""){
            add_empty_part_form(category);
        }
    })

}

async function add_empty_part_form(category) {
    part_forms = document.querySelector("#parts-forms");

    new_part_form = await fetch('/abm_testpart_layout?' + new URLSearchParams({
        category: category.options[category.selectedIndex].text,
        part_number: part_number
    }))
    new_part_form = await new_part_form.text();

    await (part_forms.insertAdjacentHTML("beforeend", new_part_form));

    document.querySelector(`#add-part-btn-${part_number}`).addEventListener("click", function () {
        document.querySelector(`#add-question-${question_number}`).style.display = "none"
        document.querySelector(`#delete-question-${question_number}`).style.display = "none"
        document.querySelector(`#add-part-btn-${part_number}`).style.display = "none"

        question_number += 1
        starting_part_question = question_number
        part_number += 1
        add_empty_part_form(category)
    })
    
    add_empty_question_form(category);
}

async function add_empty_question_form(category) {
    question_forms = document.querySelector(`#question-forms-${part_number}`)

    new_question_form = await fetch('/abm_question_layout?' + new URLSearchParams({
        category: category.options[category.selectedIndex].text,
        question_number: question_number,
        part_number: part_number
    }))
    new_question_form = await new_question_form.text();

    await (question_forms.insertAdjacentHTML("beforeend",new_question_form));

    if (question_number == starting_part_question) {
        document.querySelector(`#delete-question-${question_number}`).style.display = "none"
    }

    document.querySelector(`#add-question-${question_number}`).addEventListener("click", function () {
        document.querySelector(`#add-question-${question_number}`).style.display = "none"
        document.querySelector(`#delete-question-${question_number}`).style.display = "none"
        question_number += 1
        add_empty_question_form(category);
    })

    document.querySelector(`#delete-question-${question_number}`).addEventListener("click", function () {
        document.querySelector(`#question-form-${part_number}-${question_number}`).remove();
        question_number -= 1;
        document.querySelector(`#add-question-${question_number}`).style.display = "inline"
        if (question_number != starting_part_question) {
            document.querySelector(`#delete-question-${question_number}`).style.display = "inline"
        }
    })
}
