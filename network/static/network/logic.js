
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


