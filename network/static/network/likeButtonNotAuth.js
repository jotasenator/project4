console.log( 'likeButtonNotAuth.js loaded' );


window.addEventListener( "load", () =>
{
    disabledLikeButtons();
} );

// Disable like buttons
const disabledLikeButtons = () =>
{
    const likeButtons = document.querySelectorAll( '.like-button' );
    likeButtons.forEach( button =>
    {
        button.disabled = true;
        button.style.cursor = 'default';
        button.style.opacity = 0.2;
    } );
};