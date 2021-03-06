let part_number = 1
let question_number = 1
let starting_part_question = 1
let category_name = ""

document.addEventListener('DOMContentLoaded', function () {

    // If the page is new test, load the new test form
    new_test = document.querySelector("#test-form")
    if (new_test){
        add_empy_new_test_form()
    }

    // If the page has the edit button, create the edit test form and populate with existing data
    edit_btn = document.querySelector("#edit-btn")
    if (edit_btn){
        edit_btn.addEventListener("click", () => {
            edit_btn.style.display = "none"
            edit_test(edit_btn.value)
        })
    }
})

async function add_empy_new_test_form() {
    new_test_form = await fetch('/test_form_layout/test')
    new_test_form = await new_test_form.text()
    
    await (document.querySelector("#test-form").innerHTML = new_test_form)

    category = document.querySelector("#test-category > select")
    
    category.addEventListener("change",() => {
        document.querySelector("#parts-forms").innerHTML = ""
        if (category.options[category.selectedIndex].text != ""){
            category_name = category.options[category.selectedIndex].text
            add_empty_part_form();
        }
    })
}

// Generates a new empty part form
async function add_empty_part_form() {
    // Create new part form
    part_forms = document.querySelector("#parts-forms");

    // Get HTML for part form
    new_part_form = await fetch('/test_form_layout/test_part?' + new URLSearchParams({
        category: category_name,
        part_number: part_number
    }))
    new_part_form = await new_part_form.text();

    await (part_forms.insertAdjacentHTML("beforeend", new_part_form));
    document.querySelector(`#part-form-${part_number}`).style.animationPlayState = 'running';

    document.querySelector(`#add-part-btn-${part_number}`).addEventListener("click", () => add_new_part())
    
    await add_empty_question_form();
}

// Hides unwanted buttons and sets the variables for creating a new part form. Then generates a new empty part form
async function add_new_part() {
    document.querySelector(`#add-question-${question_number}`).style.display = "none"
    document.querySelector(`#delete-question-${question_number}`).style.display = "none"
    document.querySelector(`#add-part-btn-${part_number}`).style.display = "none"

    question_number += 1
    starting_part_question = question_number
    part_number += 1
    await add_empty_part_form()
}

// Generates a new empty question form
async function add_empty_question_form() {
    // Create question form
    question_forms = document.querySelector(`#question-forms-${part_number}`)

    // Get HTML for question form
    new_question_form = await fetch('/test_form_layout/question?' + new URLSearchParams({
        category: category_name,
        question_number: question_number,
        part_number: part_number
    }))
    new_question_form = await new_question_form.text();

    await (question_forms.insertAdjacentHTML("beforeend",new_question_form));
    document.querySelector(`#question-form-${part_number}-${question_number}`).style.animationPlayState = 'running';

    if (question_number == starting_part_question) {
        document.querySelector(`#delete-question-${question_number}`).style.display = "none"
    }

    // Events for adding/deleting questions
    document.querySelector(`#add-question-${question_number}`).addEventListener("click", () => add_new_question())

    document.querySelector(`#delete-question-${question_number}`).addEventListener("click", function () {
        document.querySelector(`#question-form-${part_number}-${question_number}`).remove();
        question_number -= 1;
        document.querySelector(`#add-question-${question_number}`).style.display = "inline"
        if (question_number != starting_part_question) {
            document.querySelector(`#delete-question-${question_number}`).style.display = "inline"
        }
    })
}

// Hides unwanted buttons and sets the variables for creating a new question form. Then generates a new empty question form
async function add_new_question() {
    document.querySelector(`#add-question-${question_number}`).style.display = "none"
    document.querySelector(`#delete-question-${question_number}`).style.display = "none"
    question_number += 1
    await add_empty_question_form();
}

// Generates test edition form and populates it with existing data
async function edit_test(id) {

    // Retrieve test data (Title, category, parts (and parts info), questions (and questions info))
    test_data = await fetch(`/get_test/${id}`)
    test_data = await test_data.json();

    category_name = test_data.category_name

    document.querySelector("#view-test-section").style.display = 'none';
    document.querySelector("#edit-test-view").innerHTML = '<div id="test-form"></div>';

    // Add an empty test form
    await add_empy_new_test_form();
    // Change texts and action form
    document.querySelector("#form-title").innerHTML = "Edit test"
    document.querySelector("#main-form").action = `/edit_test/${id}`
    document.querySelector("#confirm-button").innerHTML = "Save"

    // Fill test form with existing data
    input_title = document.querySelector("#test-form-title > input")
    input_title.value = test_data.title

    select_category = document.querySelector("#test-category > select")
    select_category.value = test_data.category_id
    select_category.setAttribute("disabled", "disabled")

    // Add Part 1 form and its questions forms
    await add_empty_part_form()

    current_question_answers = test_data.parts[part_number-1].questions[question_number-1].correct_answers
    document.querySelector(`#correct-answers-${part_number}-${question_number}`).value = current_question_answers
    
    for (var i = 1; i < Object.keys(test_data.parts[0].questions).length; i++) {
        await add_new_question()
        current_question_answers = test_data.parts[part_number-1].questions[question_number-1].correct_answers
        document.querySelector(`#correct-answers-${part_number}-${question_number}`).value = current_question_answers
    }

    // Add Parts 2, 3, ... and its questions forms (and fill with existing data)
    for (var i = 1; i < Object.keys(test_data.parts).length; i++) {
        await add_new_part()
        for (var j = 1; j < Object.keys(test_data.parts[part_number-1].questions).length; j++) {
            await add_new_question()
            current_question_answers = test_data.parts[part_number-1].questions[question_number-1-starting_part_question].correct_answers
            document.querySelector(`#correct-answers-${part_number}-${question_number-1}`).value = current_question_answers
        }
        current_question_answers = test_data.parts[part_number-1].questions[question_number-starting_part_question].correct_answers
        document.querySelector(`#correct-answers-${part_number}-${question_number}`).value = current_question_answers
    }

    // Fill part form with existing data
    for (var i = 0; i < part_number; i++) {
        document.querySelector(`#text-content-${i+1}`).value = test_data.parts[i].content
        document.querySelector(`#is-multiple-choice-${i+1}`).checked = test_data.parts[i].is_multiple_choice
        document.querySelector(`#max-score-per-answer-${i+1}`).value = test_data.parts[i].max_score_per_answer 
    }

    // Hide unwanted buttons
    document.querySelector(`#add-part-btn-${part_number}`).style.display = "none"
    document.querySelector(`#add-question-${question_number}`).style.display = "none"
    document.querySelector(`#delete-question-${question_number}`).style.display = "none"

}

// Save the student's answers when pressing next, previous or finish.
async function save_current_answers(assignment_id, finish, url) {
    answers = {}

    document.querySelectorAll(".question_number").forEach(question_num => {
        answers[question_num.innerHTML] = document.querySelector(`#answer-${question_num.innerHTML}`).value
    })
    var csrfToken = await document.getElementById("csrfToken").value
    var part_number = await document.querySelector("#part-number").value
    await fetch(`/answer/${assignment_id}`, {
        method: 'PUT',
        headers:{'X-CSRFToken': csrfToken},
        body: JSON.stringify({
            finish: finish,
            part_number: part_number,
            answers: answers
        })
    })
    location.href = url
}
