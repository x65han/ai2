import React from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faChevronDown } from '@fortawesome/free-solid-svg-icons';
import './LoadMoreButton.css';

interface Props {
    onAction: () => void,
}

class LoadMoreButton extends React.PureComponent<Props> {
    render() {
        const { onAction } = this.props;

        return (
            <div className="buttonContainer" onClick={onAction}>
                <div className="textAlignCenter">
                    ...Click to Load More...
                </div>
                <div className='textAlignCenter'>
                    <FontAwesomeIcon icon={faChevronDown} size="lg" />
                </div>
            </div>
        );
    }
}

export default LoadMoreButton;
