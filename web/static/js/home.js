/** Default configuration **/

Coloris({
    parent: '.container',
    el: '.coloris',
    wrap: false,
    theme: 'large',
    themeMode: 'light',
    margin: 0,
    format: 'hex',
    formatToggle: false,
    alpha: false,
    forceAlpha: false,
    swatchesOnly: false,
    focusInput: false,
    selectInput: false,
    swatches: [
        '#3E474E',
        '#132ED1',
        '#71491D',
        '#39FEDD',
        '#13802C',
        '#4EEF38',
        '#F17D0C',
        '#EC54BB',
        '#6C2FBC',
        "#C51211",
        "#D6DFF1",
        "#F6F657",
        "#1D9853",
    ],
    inline: true,
    defaultColor: '#C51211'
});


function shadeColor(color, percent) {
    let R = parseInt(color.substring(1, 3), 16);
    let G = parseInt(color.substring(3, 5), 16);
    let B = parseInt(color.substring(5, 7), 16);

    R = parseInt(R * (100 + percent) / 100);
    G = parseInt(G * (100 + percent) / 100);
    B = parseInt(B * (100 + percent) / 100);

    R = (R < 255) ? R : 255;
    G = (G < 255) ? G : 255;
    B = (B < 255) ? B : 255;

    R = Math.round(R / 10) * 10
    G = Math.round(G / 10) * 10
    B = Math.round(B / 10) * 10

    let RR = ((R.toString(16).length === 1) ? "0" + R.toString(16) : R.toString(16));
    let GG = ((G.toString(16).length === 1) ? "0" + G.toString(16) : G.toString(16));
    let BB = ((B.toString(16).length === 1) ? "0" + B.toString(16) : B.toString(16));

    return "#" + RR + GG + BB;
}


/** Events **/

// Listen to the "coloris:pick" event to get the picked color.
document.addEventListener('coloris:pick', function (e) {
    const color = e.detail.color;
    const darkenedColor = shadeColor(color, -26);
    const svg = document.getElementById('among-us');
    svg.querySelectorAll('.main-color').forEach(function (el) {
        el.style.fill = color;
    });
    svg.querySelectorAll('.second-color').forEach(function (el) {
        el.style.fill = darkenedColor;
    });
    svg.querySelectorAll('.second-color-stroke').forEach(function (el) {
        el.style.stroke = darkenedColor;
    });
});
