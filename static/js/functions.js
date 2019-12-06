 function getFocus() {
     setTimeout(function() {
         $('#developer_field_modal').focus();
     }, 500);
 }

 function displaySpinner() {
     $("#myloader").html(`  <div class="preloader-wrapper small active">
                <div class="spinner-layer spinner-green-only">
                  <div class="circle-clipper left">
                    <div class="circle"></div>
                  </div><div class="gap-patch">
                    <div class="circle"></div>
                  </div><div class="circle-clipper right">
                    <div class="circle"></div>
                  </div>
                </div>
              </div>`);

 }

 function displayToast(myString, myString2) {
     var str = myString;
     var str2 = myString2
     M.toast({ html: str.valueOf() + ' ' + str2.valueOf(), displayLength: 6000 })
 }

 function goBack() {
     window.history.back();
 }

 //called from userPrompt() below. If user agrees to delete then this function calls the Flask delete URL
 function deleteGame(id) {
     request = $.ajax({
         url: "/delete_game" + "/" + id,
         type: "GET",
         data: $('#myDeleteModal').modal('close'),
         complete: setTimeout(displayToast("Game", "deleting..."), 3000) //Timeout used for user experience.
     });
 }
 // /same as deleteGame. 
 // TODO: combine these two functions for one reuseable delete function.
 function deleteDeveloper(id) {
     request = $.ajax({
         url: "/delete_developer" + "/" + id,
         type: "GET",
         data: $('#myDeleteModal').modal('close'),
         complete: displaySpinner()

     });
 }

 function userPrompt(id, name) {
     $("#myDeleteModal").modal('open');
     $("#delete_name").empty();
     $("#delete_name").append(name);

     $("#delete_game_btn").click(function() {
         $(this).data('clicked', true);
         displaySpinner();
         deleteGame(id);
     });

     $("#delete_developer_btn").click(function() {
         $(this).data('clicked', true);
         deleteDeveloper(id)
     });
 }

 // Refreshes the artist select drop-down list after a new artist is added.
 function reloadList() {
     request = $.ajax({
         url: "/modal_create_developer",
         type: "POST",
         data: $("#developer_field_modal"),
     });

     request.done(function(data) {
         $('.developer_section').css("background-color", "#FFFF9C").effect("pulsate", { times: 6 }, 2000).animate({ backgroundColor: "#FFFFFF" }, 6500);
         $('.developer_section').html(data)
         $('select').formSelect();
         displayToast("Developer", "added!");
     });
 };
 // TO DO: create one resuable function for calling modals.
 // function callModal() {
 //     $('p.activator').mouseover(function(e) {
 //         $(this).trigger('#callModal');
 //     });
 // }
 