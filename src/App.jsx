import { useState, useEffect } from 'react'
import './App.css'

function App() {
  const [allExtensions, setAllExtensions] = useState([]); 
    // needed when we are displaying inactive and want to display active or all
  const [displayedExt, setDisplayedExt] = useState([]);
  const [extsShowed, setExtsShowed] = useState("all");
  const [theme, setTheme] = useState("light");

  useEffect(() => {
    getData();

    const savedTheme = localStorage.getItem("theme") || "light";
    setTheme(savedTheme);
    if (savedTheme === "dark") {
      document.documentElement.classList.add("dark");
    } else {
      document.documentElement.classList.remove("dark");
    }
  }, []);

  const getData = async () => {
    try{
      const response = await fetch("../data.json");
      const data = await response.json();
      setAllExtensions(data);
      setDisplayedExt(data);
    } catch (err) {
      console.log(err);
    }
  };  

  const toggleLightDarkMode = () => {
    const isDark = document.documentElement.classList.toggle("dark");
    setTheme(isDark ? "dark" : "light");
  }

  const showAll = () => {
    setDisplayedExt(allExtensions);
    setExtsShowed("all");
  };

  const showActive = () => {
    setDisplayedExt(allExtensions);
    setDisplayedExt((prev) => prev.filter(extension => extension.isActive === true));
    setExtsShowed("active");
  };

  const showInactive = () => {
    setDisplayedExt(allExtensions);
    setDisplayedExt((prev) => prev.filter(extension => extension.isActive !== true));
    setExtsShowed("inactive");
  };

  const removeItem = (toRemove) => {
    setAllExtensions((prev) => prev.filter(extension => extension !== toRemove));
    setDisplayedExt((prev) => prev.filter(extension => extension !== toRemove));
  };

  const changeActive = (toChange) => {
    const newExtension = toChange;
    newExtension.isActive = !toChange.isActive;
    setAllExtensions((prev) => prev.map((extension) => {
      if(extension === toChange) {
        return newExtension;
      } else {
        return extension;
      }
    }));
    setDisplayedExt((prev) => prev.map((extension) => {
      if(extension === toChange) {
        return newExtension;
      } else {
        return extension;
      }
    }));
  }

  return (
    <div className="bg-[image:var(--light-gradient)] dark:bg-[image:var(--dark-gradient)]">
      <div className="flex justify-between rounded-xl bg-[var(--neutral-0)] dark:bg-[var(--neutral-800)] px-3 py-2 shadow-sm">
        <div className="">
          <img src="../assets/images/logo.svg" className=""/>
        </div>
        <button className="rounded-xl px-3 py-3 bg-[var(--neutral-100)] dark:bg-[var(--neutral-700)] 
          hover:bg-[var(--neutral-300)] dark:hover:bg-[var(--neutral-600)] focus:outline-2 focus:outline-offset-2 
          focus:outline-[var(--red-700)] dark:focus:outline-[var(--red-500)]" 
          onClick={toggleLightDarkMode}>
          <img src={theme === "light" ? "../assets/images/icon-moon.svg" : "../assets/images/icon-sun.svg"}/>
        </button>
      </div>

      <div className="flex flex-col sm:flex-row items-center justify-between pb-4 pt-4"> 
        <p className='text-3xl font-[700] text-[var(--neutral-900)] dark:text-[var(--neutral-0)]'>Extensions List</p>
        <div className="">
          <button className={`${
            extsShowed === "all" 
              ? "btn-filter-active"
              : "btn-filter-inactive"
            }`} 
            onClick={showAll}>
              All
          </button>
          <button className={`${
            extsShowed === "active" 
              ? "btn-filter-active"
              : "btn-filter-inactive"
            }`} 
            onClick={showActive}>
              Active
          </button>
          <button className={`${
            extsShowed === "inactive"
              ? "btn-filter-active"
              : "btn-filter-inactive"
            }`} 
            onClick={showInactive}>
              Inactive
          </button>
        </div>
      </div>
      
      <div className="grid gap-4 grid-cols-1 sm:grid-cols-2 lg:grid-cols-3">
        {displayedExt.map((extension) => (
          <div className="flex flex-col p-4 rounded-2xl h-[200px] bg-[var(--neutral-0)] dark:bg-[var(--neutral-800)] shadow-sm">
            <div className="flex items-start text-left">
              <img className="" src={extension.logo}/>
              <div className="m-3 mt-0 ">
                <h3 className="text-lg font-[700] text-[var(--neutral-900)] dark:text-[var(--neutral-0)]">{extension.name}</h3> 
                <p className="text-base font-[400] text-[var(--neutral-900)] dark:text-[var(--neutral-300)]">{extension.description}</p>
              </div>
            </div>
            
            <div className="flex items-center justify-between mt-auto">
              <button className="rounded-full px-4 py-2 shadow-sm dark:border-1 dark:border-[var(--neutral-600)] font-[400]
              bg-[var(--neutral-0)] dark:bg-[var(--neutral-800)] hover:bg-[var(--red-700)] hover:text-[var(--neutral-0)]
              dark:hover:bg-[var(--red-400)] dark:hover:text-[var(--neutral-900)] focus:outline-2 focus:outline-offset-2 
              focus:outline-[var(--red-700)] dark:focus:outline-[var(--red-500)]
              text-[var(--neutral-900)] dark:text-[var(--neutral-100)]" 
                onClick={() => removeItem(extension)}>
                  Remove
              </button>
              <label className="inline-flex items-center cursor-pointer">
                <input 
                  type="checkbox" 
                  className="sr-only peer" 
                  checked={extension.isActive} 
                  onChange={() => changeActive(extension)}
                />
                <div className="relative w-11 h-6 bg-[var(--neutral-300)] peer-focus:outline-none peer-focus:ring-4 
                  peer-focus:ring-[var(--red-400)] dark:peer-focus:ring-[var(--red-400)] rounded-full peer dark:bg-gray-700 
                  peer-checked:after:translate-x-full rtl:peer-checked:after:-translate-x-full peer-checked:after:border-white 
                  after:content-[''] after:absolute after:top-[2px] after:start-[2px] after:bg-white after:border-gray-300 
                  after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 
                  peer-checked:bg-[var(--red-700)] dark:peer-checked:bg-[var(--red-400)] focus:outline-2 focus:outline-offset-2 
                  focus:outline-[var(--red-700)] dark:focus:outline-[var(--red-500)]
                  peer-checked:hover:bg-[var(--red-500)] dark:peer-checked:hover:bg-[var(--red-500)]"/>
              </label>
            </div>
          </div>
        ))}
      </div>
      

    </div>
  )
}

export default App
