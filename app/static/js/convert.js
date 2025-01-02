FilePond.setOptions({
    server: {
        process: {
            url: '/convert',
            method: 'POST',
            onload: (response) => {
                return response;
            },
        },
    },
    labelIdle: 'Drag & Drop your files or <span class="filepond--label-action"> Browse </span> <div>allowed filetypes: .py, .zip</div>',
});

FilePond.create(
    document.querySelector('input'),
    {
        instantUpload: true,
    }
);

document.querySelector(".filepond").addEventListener("FilePond:processfile", (e) => {
    if (e.detail.error) return
    let response = e.detail.file.serverId
    window.location.href = `/convert/${response}`
})