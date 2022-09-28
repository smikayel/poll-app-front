const options = document.querySelectorAll('input[class="poll-chooes"]');


const deleteOthers = (e) => {
  const options = document.querySelectorAll('input[class="poll-chooes"]');
  for (let option of options) {
    option.removeAttribute('checked');
  }
  e.target.setAttribute('checked', "");
}

for (let option of options) {
  option.addEventListener('click', deleteOthers);
}