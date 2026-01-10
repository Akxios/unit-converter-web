const categorySelect = document.getElementById('category');
const fromSelect = document.getElementById('from');
const toSelect = document.getElementById('to');
const valueInput = document.getElementById('value');
const resultOutput = document.getElementById('result');
const convertBtn = document.getElementById('convertBtn');

const API_URL = window.location.origin;

// Загрузка единиц
async function loadUnits() {
  const category = categorySelect.value;
  const res = await fetch(`${API_URL}/units/${category}`);

  if (!res.ok) {
    alert("Failed to load units");
    return;
  }
  const data = await res.json();

  fromSelect.innerHTML = '';
  toSelect.innerHTML = '';

  data.units.forEach(unit => {
    const optionFrom = document.createElement('option');
    optionFrom.value = unit;
    optionFrom.textContent = unit;
    fromSelect.appendChild(optionFrom);

    const optionTo = document.createElement('option');
    optionTo.value = unit;
    optionTo.textContent = unit;
    toSelect.appendChild(optionTo);
  });
}

// Конвертация
async function convertValue() {
    const category = categorySelect.value;
    const value = parseFloat(valueInput.value);
    if (isNaN(value)) {
        alert("Введите корректное число!");
        return;
    }

    const from_unit = fromSelect.value;
    const to_unit = toSelect.value;

    const response = await fetch(`${API_URL}/convert`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ category, value, from_unit, to_unit })
    });

    if (!response.ok) {
        alert("Ошибка при конверсии");
        return;
    }

    const data = await response.json();
    // Показываем результат с единицей
    resultOutput.classList.remove("placeholder");
    resultOutput.innerText = `Result: ${data.result} ${data.result_unit}`;
}

// События
categorySelect.addEventListener('change', loadUnits);
convertBtn.addEventListener('click', convertValue);

// Инициализация
loadUnits();
