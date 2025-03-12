import { useState, useEffect } from "react";
import "./App.css";
// const BACKEND_URL = import.meta.env.BACKEND_URL || "http://localhost:8085";
const BACKEND_URL = "https://yoga-app-backend-746688919465.us-east1.run.app"
// const BACKEND_URL = "http://localhost:8085"

function App() {
  const [selectedImage, setSelectedImage] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [relatedPoseImages, setRelatedPoseImages] = useState({});

  const handleImageChange = (event) => {
    if (event.target.files && event.target.files[0]) {
      setSelectedImage(event.target.files[0]);
      setPrediction(null);
      setError(null);
      setRelatedPoseImages({});
    }
  };

  const handleUpload = async () => {
    if (!selectedImage) {
      setError("Please select an image.");
      return;
    }

    setIsLoading(true);
    setError(null);
    setPrediction(null);
    setRelatedPoseImages({});

    const formData = new FormData();
    formData.append("file", selectedImage);

    try {
      const response = await fetch(
        `${BACKEND_URL}/api/identify-pose/`,
        {
          method: "POST",
          body: formData,
        }
      );

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Failed to identify pose.");
      }

      const data = await response.json();
      setPrediction(data);
    } catch (err) {
      console.error("Error uploading image:", err);
      setError(err.message || "An error occurred while uploading the image.");
    } finally {
      setIsLoading(false);
    }
  };
    
  useEffect(() => {
    const fetchRelatedPoseImages = async () => {
      if (prediction && prediction.related_poses && prediction.related_poses.length > 0) {
        try {
          const response = await fetch(
            `${BACKEND_URL}/api/pose-images/`,
            {
              method: "POST",
              headers: {
                "Content-Type": "application/json",
              },
              body: JSON.stringify(prediction.related_poses),
            }
          );

          if (!response.ok) {
            throw new Error("Failed to fetch related pose images.");
          }

          const data = await response.json();
          setRelatedPoseImages(data);
        } catch (err) {
          console.error("Error fetching related pose images:", err);
          setError("Failed to fetch related pose images.");
        }
      }
    };

    fetchRelatedPoseImages();
  }, [prediction]);

  return (
    <div className="app-container">
      <h1>Yoga Pose Identifier</h1>
      <div className="upload-section">
        <input
          type="file"
          accept="image/*"
          onChange={handleImageChange}
          id="image-upload"
        />
        <label htmlFor="image-upload" className="upload-label">
          Choose an Image
        </label>
        {selectedImage && (
          <div className="image-preview">
            <img
              src={URL.createObjectURL(selectedImage)}
              alt="Uploaded"
              className="preview-image"
            />
          </div>
        )}
        <button
          onClick={handleUpload}
          disabled={isLoading}
          className="upload-button"
        >
          {isLoading ? "Identifying..." : "Identify Pose"}
        </button>
      </div>
      {error && <div className="error-message">{error}</div>}
      {prediction && (
        <div className="prediction-section">
          <h2>Pose Identification:</h2>
          {prediction.pose_name && (
            <p>
              This pose looks like: <b>{prediction.pose_name}</b>
            </p>
          )}
          {prediction.alternate_names &&
            prediction.alternate_names.length > 0 && (
              <div>
                <h4>Alternate Names:</h4>
                <ul>
                  {prediction.alternate_names.map((name, index) => (
                    <li key={index}>{name}</li>
                  ))}
                </ul>
              </div>
            )}
          {prediction.related_poses && prediction.related_poses.length > 0 && (
            <div>
              <h4>Related Poses:</h4>
              <div className="related-poses-container">
                {prediction.related_poses.map((pose, index) => {
                  const imageUrl = relatedPoseImages[pose];
                  return (
                    <div key={index} className="related-pose-item">
                     {imageUrl ? (
                          <a href={imageUrl} target="_blank" rel="noopener noreferrer">
                           <img
                              src={imageUrl}
                              alt={pose}
                              className="related-pose-image"
                            />
                          </a>
                        ): <div>Image Loading ... </div>}
                      <p className="related-pose-name">{pose}</p>
                     
                    </div>
                  );
                })}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default App;
