/* Questionnaire de dépistage auditif */
var result = "";
var commentaire = "";
var j = 1;
var y = 0;
var response = [];

/* passage à l'étape suivante */
$('#next-stage').click(function() {
  
// Pour ne pas laisser l'utilisateur continuer avec le bouton suivant s'il n'a pas checké une réponse
if (!$("input[name=q" + j + "]:checked").val()) {
   /*alert('Check une réponse d\'abord !');*/
   $('p.error').css('display','block');
}
else
{
  // Pour sélectionner le prochain "stage"
  $('input[name="stage"]').nextAll().eq(y).prop("checked", true);
  // On ajoute la réponse de l'utilisateur dans le tableau response
  response["q" + j] = $("input[name=q" + j + "]:checked").val();
  changeButtonResult();
  console.log(response);
  // On incrémente les variables pour y compter les "stages" et les reponses
  if(j < 5) j++;
    
  y++;
  //passe en display none pour ne pas gêner
  $('p.error').css('display','none');

}
  
});

  /* passage à l'étape suivante */
$('.stage').click(function() {
  
//y = parseInt($(this).index() - 2) ;
//alert(y);
j = ($(this).index());
y = parseInt($(this).index() - 1);

if (parseInt($(this).index() - 1) > y) 
{
   //alert('Check une réponse d\'abord !');
}
else
{
  // Pour sélectionner le prochain "stage"
  //$('input[name="stage"]').nextAll().eq(y).prop("checked", true);

}

});

//response["q" + j] = $("input[name=q" + j + "]:checked").val();
$('input:radio').click(function() {
  if(($(this).attr('name')) == 'q'+ j)
  {
    response["q" + j] = $(this).val();
    changeButtonResult();
    console.log(response);
  }
});

// Fonction qui va calculer les points
function getPoints(params)
{
var r = 0;

  for(var i in params)
  {
    if(params[i] == 'oui')
      r++;
  }
  
return r;
  
}

function changeButtonResult()
{
if (getLengthObj(response) == 5) {
    $('#next-stage').html('Valider');
    result = getPoints(response);
    commentaire = getResponseQuiz(result);
      $('#next-stage').click(function() {
      $('#result').css('display','block');
      $('html, body').animate({
        scrollTop: $("#result").offset().top-200
        }, 2000);
      $('#result p').html(commentaire);
      });
  }
}
 // Fonction qui va donner le résultat
function getResponseQuiz(params)
{
var commentaire;

switch (params) {
    case 0: commentaire = "Il semblerait que vous n'ayez aucun problème d'audition. Mais si toutefois vous avez un doute, vous pouvez prendre rendez-vous avec notre audioprothésiste pour un bilan complet et gratuit.";
    break;

    case 1: 

    case 2: commentaire = "Au vu de vos résultats, il semblerait que vous ne rencontriez pas de problème majeur dans la vie courante, mais ce questionnaire ne remplace en aucun cas un dépistage auditif. Nous vous conseillons donc de venir voir notre audioprothésiste pour un bilan complet et gratuit.";
    break;

    case 3: 

    case 4: commentaire = "Il semblerait que vous rencontriez des difficultés dans certains cas de la vie courante, nous vous conseillons de venir faire un bilan auditif gratuit auprès de notre audioprothésiste.";
    break;

    case 5: commentaire = "Au vu de vos résultats, il semblerait que vous rencontriez des difficultés dans la plupart des situations de la vie courante. Nous vous recommandons fortement de faire un bilan auditif gratuit auprès de notre audioprothésiste car ce questionnaire ne remplace en aucun cas un vrai bilan.";
    break;

    default:  commentaire = "Voulez-vous refaire le test ?";
  
    }
  
  return commentaire;
}
  
function getLengthObj(array)
{
 var size = 0;
for (key in array) {
      if (array.hasOwnProperty(key)) size++;
  }
  return size;
}