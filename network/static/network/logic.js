
console.log( 'logic.js loaded' );


window.addEventListener( "load", () =>
{
    likeButton();
    editPostText( postText );
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
    // obtain security token from page!!!
    const csrftoken = document.cookie.split( ';' ).find( cookie => cookie.trim().startsWith( 'csrftoken=' ) ).split( '=' )[ 1 ];

    const postTextElement = event.target.parentElement.querySelector( '.text' );

    // Create textarea element with the current post text
    const textarea = document.createElement( 'textarea' );
    textarea.value = postText;

    //Replace text from post wiht previous textarea element
    postTextElement.replaceWith( textarea );

    // Create button save
    const saveButton = document.createElement( 'button' );
    saveButton.innerText = 'Save';

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
            } );
    } );

    // Add button after textarea
    textarea.insertAdjacentElement( 'afterend', saveButton );
}



