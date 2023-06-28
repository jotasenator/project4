
console.log( 'logic.js loaded' );


window.addEventListener( "load", () =>
{
    likeButton();
} );

// Like button logic
// Need to have them all
const likeButton = () => document.querySelectorAll( ".like-button" ).forEach( ( button ) =>
{
    button.addEventListener( "click", () =>
    {
        const postId = button.dataset.postId;
        console.log( `button clicked for post ${ postId }` );

        fetch( `/like/${ postId }` )
            .then( ( response ) => response.json() )
            .then( ( data ) =>
            {

                document.querySelector( `#likes-${ postId }` ).innerHTML = data.likes;
            } );
    } );
} );

const editPostText = ( postText ) =>
{
    console.log( 'editPostText called!!!' );
    // obtain security token from page!!!
    const csrftoken = document.cookie.split( ';' ).find( cookie => cookie.trim().startsWith( 'csrftoken=' ) ).split( '=' )[ 1 ];

    const postTextElement = event.target.parentElement.querySelector( '.text' );

    // Hide the "Edit" button
    const editButton = event.target;
    editButton.classList.add( "d-none" );

    // Create textarea element with the current post text
    const textarea = document.createElement( 'textarea' );
    textarea.value = postText;
    textarea.classList.add( 'form-control', 'ml-3' );
    //add this calculation to avoid overlapping and to remain the same if page shrinks
    textarea.style.width = 'calc(99% - 1rem)';

    //Replace text from post wiht previous textarea element
    postTextElement.replaceWith( textarea );

    // Create button save
    const saveButton = document.createElement( 'button' );
    saveButton.innerText = 'Save';
    saveButton.classList.add( 'btn', 'btn-primary', 'ml-3', 'mt-3' );

    // Add fetch event to save button
    saveButton.addEventListener( 'click', () =>
    {
        // Obtain new content from textarea
        const newPostText = textarea.value;

        // Fetch request to /editPost
        fetch( '/editPost', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify( {
                post_text: newPostText
            } )
        } )
            .then( response => response.json() )
            .then( data =>
            {
                // replace content
                textarea.replaceWith( postTextElement );
                postTextElement.innerText = newPostText;

                // Remove the "Save" button
                saveButton.remove();

                // Show the "Edit" button again
                editButton.classList.remove( "d-none" );

            } );
    } );

    // Add button after textarea
    textarea.insertAdjacentElement( 'afterend', saveButton );

    //can not call the onclickOut as anonymous function for removing it after, so need to use this wrapper
    const onClickOutWrapper = ( event ) => onClickOut( event, textarea, saveButton, editButton, postTextElement, onClickOutWrapper );

    setTimeout( () =>
    {
        document.addEventListener( 'click', onClickOutWrapper );

    }, 0 );

};

//click out textarea or save button will cancel the edit
const onClickOut = ( event, textarea, saveButton, editButton, postTextElement, onClickOutWrapper ) =>
{
    if ( event.target !== textarea && event.target !== saveButton &&
        !textarea.contains( event.target ) &&
        !saveButton.contains( event.target ) )
    {
        console.log( 'onClickOut called!!!' );
        document.removeEventListener( 'click', onClickOutWrapper );
        textarea.replaceWith( postTextElement );
        saveButton.remove();
        editButton.classList.remove( "d-none" );

    }
}

