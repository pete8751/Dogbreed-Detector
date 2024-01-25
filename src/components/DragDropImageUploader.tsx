import React, {useState, useRef, useEffect} from 'react';

interface Image {
    file: File;
    name: string;
    url: string;
}

interface predictObject {
    breed: string;
    probability: number; // Assuming the percentage is represented as a number (0 to 100)
  };

function DragDropImageUploader() {
    const dragArea = document.querySelector(".drag-area");

    const [image, setImage] = useState<Image | null>(null);
    //Prediction is an array of objects, each object has a key and value, where key is the breed name and value is the probability there are 5 objects in the array
    const [prediction, setPrediction] = useState<predictObject[]>([]);
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
                file: file,
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
        // I want to check if the file is a JPEG or PNG file
        if (file.type !== 'image/jpeg' && file.type !== 'image/png') {
            alert("Only JPEG and PNG files are supported.");
            return;
        }
  
        //I want to check if file width is less than 1920p, and height is less than 1080p
        // if (file.width > 1920 || file.height > 1080) {
        //     alert("Image size must be less than 5MB.");
        //     return;
        // }
        // console.log(image?.name)
        // console.log(file)

        if (!image || !(image.name === file.name)) {
            setImage({
                file: file,
                name: file.name,
                url: URL.createObjectURL(file),
            });
        }
    }

    function uploadImage() {
        const imageUrl = image?.url; 
        const file = image?.file;
        console.log(file)
    
        if (!imageUrl) {
            console.error('Image URL is missing.');
            return;
        }
        if (!file) {
            console.error('File is missing.');
            return;
        }
    
        // Example server endpoint, replace with your actual server endpoint
        const serverEndpoint = 'https://dogbreed-ml-model-dock-fa3461448856.herokuapp.com/analyze_image';
    
        // Create a FormData object
        const formData = new FormData();
        formData.append('imageUrl', imageUrl);
        formData.append('file', file);

        const reader = new FileReader();

        // Make the POST request using fetch
        fetch(serverEndpoint, {
            method: 'POST',
            body: formData,  // Use FormData instead of JSON.stringify
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
            setPrediction(responseData.Prediction);
        })
        .catch(error => {
            console.error('Error during fetch operation:', error);
        });
        console.log(reader.readAsArrayBuffer(file))
    }

  // useEffect to listen for changes in predictState
    useEffect(() => {
    // This function will be called whenever predictState changes

    }, [prediction]);

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
            <div className="predict-container">
                <div className="prediction">
                    {prediction &&
                    (<p>
                        This is a {prediction[0].breed}
                    </p>)}
                </div>
                <div className="breakdown">
                {prediction &&
                    prediction.map((item) => (
                    <p key={item.breed}>
                        This is {Math.round(item.probability * 100)}% a {item.breed}
                    </p>
                    ))}
                </div>
            </div>
        </div>
    )
}

export default DragDropImageUploader;