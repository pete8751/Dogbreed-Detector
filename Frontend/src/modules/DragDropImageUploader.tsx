

function DragDropImageUploader() {
    return (
        <div className = "card">
            <div className="top">
                <p>Drag & Drip your image</p>
            </div>
            <div className="drag-area">
                <span className = "select">
                    Drop Images Here
                </span>
                Drag & Drop images here or {" "}
                <span className="select">
                    Browse
                </span>
                <input type="file" name="file" className="file" />
            </div>
            <div className="container">
                <div className="image">
                    <span className="delete">&times;</span>
                </div>
                <img src="" alt="" />
            </div>
            <button type="button">
                Upload
            </button>
        </div>
    )
}