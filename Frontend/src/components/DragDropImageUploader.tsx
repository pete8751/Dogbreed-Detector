import React, {useState, useRef} from 'react';

interface Image {
    name: string;
    url: string;
}

function DragDropImageUploader() {
    const dragArea = document.querySelector(".drag-area");

    const [image, setImage] = useState<Image | null>(null);
    const [isDragging, setIsDragging] = useState(false);
    const fileInputRef = useRef<HTMLInputElement>(null);

    if (image) dragArea?.classList.add("used");

    function selectFiles() {
        if (fileInputRef.current) {
            fileInputRef.current.click();
        }
    }

    function onFileSelect(event: any) {
        const files = event.target.files;
        if (files.length === 0) return;
        if (files.length > 1) return alert("Please select only one image.");
        const file = files[0];
        if (file.type.split('/')[0] !== 'image') return alert("Don't support this file type.");
        if (!image || !(image.name === file.name)) {
            setImage({
                name: file.name,
                url: URL.createObjectURL(file),
            });
        }
    }

    function deleteImage() {
        setImage(null);
        dragArea?.classList.remove("used");
    }

    function onDragOver(event: any) {
        event.preventDefault();
        setIsDragging(true);
        dragArea?.classList.add("active");
        event.dataTransfer.dropEffect = "copy";
    }

    function onDragLeave(event: any) {
        event.preventDefault();
        dragArea?.classList.remove("active");
        setIsDragging(false);
    }

    function onDrop(event: any) {
        event.preventDefault();
        setIsDragging(false);
        dragArea?.classList.remove("active");
        const files = event.dataTransfer.files;
        if (files.length === 0) return;
        if (files.length > 1) return alert("Please select only one image.");
        const file = files[0];
        if (file.type.split('/')[0] !== 'image') return alert("Don't support this file type.");

        if (!image || !(image.name === file.name)) {
            setImage({
                name: file.name,
                url: URL.createObjectURL(file),
            });
        }
    }

    function uploadImage() {
        const imageUrl = image?.url; // Assuming `image` is the variable holding your image object
    
        if (!imageUrl) {
            console.error('Image URL is missing.');
            return;
        }
    
        // Example server endpoint, replace with your actual server endpoint
        const serverEndpoint = 'http://127.0.0.1:5000/analyze_image';
    
        // Prepare the data to be sent in the request body
        const data = {
            imageUrl: imageUrl,
            // Add any additional data you want to send
        };
    
        // Make the POST request using fetch
        fetch(serverEndpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                // Add any additional headers if needed
            },
            body: JSON.stringify(data),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(responseData => {
            // Handle the response from the server
            console.log('Server response:', responseData);
        })
        .catch(error => {
            console.error('Error during fetch operation:', error);
        });
    }

    return (
        <div className = "card">
            <div className="top">
                <p>Drag & Drop your Image</p>
            </div>
            <div className="drag-area" onDragOver={onDragOver} onDragLeave={onDragLeave} onDrop={onDrop}>
                {image && ( 
                    <div className="display-image">
                        <span className="delete" onClick={deleteImage}>&times;</span>
                        <img src={image.url} alt={image.name} />
                    </div>
                )}
                {isDragging ? (<span className = "select_drop">
                    Drop Images Here
                </span>) : ( !image &&
                <>
                    Drag & Drop Image here or {" "}
                <span className="select" role="button" onClick={selectFiles}>
                    Browse
                </span>
                </>)}
                <input type="file" name="file" className="file" ref={fileInputRef} onChange = {onFileSelect} />
            </div>
            {/* <div className="container">
                {image && (
                    <div className="image">
                        <span className="delete" onClick={deleteImage}>&times;</span>
                        <img src={image.url} alt={image.name} />
                    </div>
                )}
            </div> */}
            <button type="button" onClick={uploadImage}>
                Analyze
            </button>
        </div>
    )
}

export default DragDropImageUploader;