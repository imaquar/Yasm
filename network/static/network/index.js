function handleTextArea(textArea) {
    submitButton = Array.from(textArea.parentElement.children).filter(el => el.tagName === "BUTTON")[0]

    if (textArea.id === "text-area-edit") {
        textArea.style.height = "20px";
    }

    if (textArea.value.length === 0) {
        submitButton.style.display = "none";
        if (textArea.id === "text-area-post") {
            textArea.style.height = "57px";
        } else if (textArea.id === "text-area-comment") {
            textArea.style.height = "46px";
        }
    } else {
        submitButton.style.display = "block";
        textArea.style.height = `${textArea.scrollHeight + 2}px`;
    }
}

function handleLike(button, entryType, entryId) {
    const likeIcon = button.children[0];
    const likeCounter = button.children[1];

    fetch(`http://localhost:8000/handlelike/${entryType}/${entryId}`)
    .then((response) => {
        if (response.redirected) {
            window.location.replace(response.url);
        } else if (likeIcon.className == "bi bi-heart") {
            likeIcon.className = "bi bi-heart-fill";
            button.className = "like-footer-button-active";
            likeCounter.innerHTML = parseInt(likeCounter.innerHTML) + 1;
        } else {
            likeIcon.className = "bi bi-heart";
            button.className = "footer-button";
            likeCounter.innerHTML = parseInt(likeCounter.innerHTML) - 1;
        }
    });
}

function toggleCommentSection(button) {
    const commentIcon = button.children[0];
    const commentSection = document.getElementById(`${button.dataset.post_id}`);
    if (commentSection.style.display === "block") {
        commentSection.style.display = "none";
        commentIcon.className = "bi bi-chat";
        button.className = "footer-button";
    } else {
        commentSection.style.display = "block"
        commentIcon.className = "bi bi-chat-fill";
        button.className = "comment-footer-button-active";
        setFocus("#text-area-comment");
    }
}

function toggleEditEntrySection(button) {
    const entryBody = button.parentElement.parentElement.parentElement.children[1];
    const editFormDiv = button.parentElement.parentElement.parentElement.children[2];
    const editForm = editFormDiv.children[0].children[0];
   
    if (entryBody.style.display == "none") {
        entryBody.style.display = "flex";
        editFormDiv.style.display = "none";
    } else {
        editForm.value = entryBody.innerHTML.trim();
        entryBody.style.display = "none";
        editFormDiv.style.display = "flex";
        editForm.focus();
    }
}

function toggleEntryButtons(entry) {
    const deleteEditButtons = entry.children[0].children[1];
    if (deleteEditButtons.style.display == "inline") {
        deleteEditButtons.style.display = "none";
    } else {
        deleteEditButtons.style.display = "inline";
    }
    
}

function handleDeleteEntry(button, entryType, entryId) {
    const entry = button.parentElement.parentElement.parentElement;

    fetch(`http://localhost:8000/delete/${entryType}/${entryId}`)
    .then(() => {
        entry.style.display = "none"
        if (entryType == "post") {
            document.getElementById(entryId).style.display = "none";
        } else {
            const counter = document.getElementById(`comment-counter-${entry.parentElement.id}`)
            counter.innerHTML = parseInt(counter.innerHTML) - 1;
        }    
    });
}

function handleEditEntry(editForm, event, entryType, entryId) {
    event.preventDefault();
    
    const textArea = editForm.children[0];
    const entryBody = editForm.parentElement.parentElement.children[1];
    const editFormDiv = editForm.parentElement;

    fetch(`http://localhost:8000/edit/${entryType}/${entryId}`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken")
        },
        body: JSON.stringify({"text": textArea.value}),
    })
        .then(() => {
            entryBody.innerHTML = textArea.value;
            entryBody.style.display = "flex";
            editFormDiv.style.display = "none";
        });
}

function handleFollow(button, reqUserId) {
    const followText = button.children[0];
    const followIcon = button.children[1];
    const followerCounter = document.getElementById("follower-counter");
    
    fetch(`http://localhost:8000/handlefollow/${reqUserId}`)
    .then(() => {
        if (followIcon.className == "bi bi-person-add") {
            followIcon.className = "bi bi-person-dash";
            followText.innerHTML = "Unfollow";
            followerCounter.innerHTML = 
                `Followers: ${parseInt(followerCounter.innerHTML.match(/(\d+)/)[0]) + 1}`;
        } else {
            followIcon.className = "bi bi-person-add";
            followText.innerHTML = "Follow";
            followerCounter.innerHTML = 
                `Followers: ${parseInt(followerCounter.innerHTML.match(/(\d+)/)[0]) - 1}`;
        }
    });
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function setFocus(inputFieldId) {
    const inputField = document.querySelector(inputFieldId);
    inputField.focus();
}

function toggleProfileBioFormButton(textarea, userId) {
    const button = document.querySelector(".profile-button");
    const form = textarea.parentElement;

    if (textarea.value.length > 0) {
        button.children[0].innerHTML = "Save";
        button.children[1].className = "bi bi-floppy";
        button.onclick = () => handleUpdateProfile(event, form, userId);
    } else {
        button.children[0].innerHTML = "Edit";
        button.children[1].className = "bi bi-pencil";
        button.onclick = () => toggleUpdateProfileSection();
    }

}

function toggleUpdateProfileSection() {
    const userUpdateForm = document.querySelector(".form-profile-grid");
    const userProfileGrid = document.querySelector(".profile-grid");
    if (userUpdateForm.style.display === "grid") {
        userUpdateForm.style.display = "none";
        userProfileGrid.style.display = "grid";
    } else {
        userUpdateForm.style.display = "grid";
        userProfileGrid.style.display = "none";
    }
}

function handleUpdateProfile(event, form, userId) {
    event.preventDefault();
    const textAreaBio = form.children[1];
    fetch(`http://localhost:8000/update/${userId}`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken")
        },
        body: JSON.stringify({"bio": textAreaBio.value}), 
    })
        .then(() => {
            window.location.replace(`http://localhost:8000/profile/${userId}`);
        })
}
